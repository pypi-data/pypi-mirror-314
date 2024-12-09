import asyncio
import logging
from typing import Any

import orjson
from psycopg import sql
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from helpers.AsynQMessage import AsynqMessage

class AsynqManager:
    delete_on_consume = False
    table_name = None
    queue_name = None
    _db_pool: AsyncConnectionPool = None
    _db_pool_function = None
    _listen_task: Any = None
    _message_queue = asyncio.Queue()

    def __init__(self, db_pool_function, queue_name: str, table_name: str = "asynq_messages"):
        self._db_pool_function = db_pool_function
        self.queue_name = queue_name
        self.table_name = table_name
        pass

    async def __aenter__(self):
        self._db_pool = self._db_pool_function(open=False)
        await self._db_pool.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._db_pool.close()
        pass

    async def queue_text(self, message: str):
        async with self._db_pool.connection() as conn:
            await conn.execute(
                sql.SQL("INSERT INTO {} (queue_name, payload) VALUES ({}, {}::json)")
                .format(sql.Identifier(self.table_name), self.queue_name, message)
            )

    async def queue_json(self, dictlike_obj: Any):
        await self.queue_text(orjson.dumps(dictlike_obj).decode("utf-8"))

    async def _enqueue_message_batch(self, limit=20, offset=0):
        '''
        Get the next message from the queue
        :return:
        '''

    async def _consume_backlog(self, json_messages):
        '''
        Iterator that catches up with all pending messages in the queue.
        Finishes iteration when no more messages to catch up
        :return:
        '''
        logging.debug(f"Catching up with backlog on queue {self.queue_name}")
        async with self._db_pool.connection() as conn:
            while True:
                async with conn.transaction():
                    cur = conn.cursor(row_factory=dict_row)
                    result = await cur.execute(
                        sql.SQL(
                            "SELECT * FROM {table_name} WHERE queue_name = {queue_name} ORDER_BY id ASC LIMIT 1 FOR UPDATE SKIP LOCKED").format(
                            table_name=sql.Identifier(self.table_name), queue_name=sql.Literal(self.queue_name)
                        )
                    )
                    message = await result.fetchone()
                    if message:
                        if json_messages:
                            logging.debug(f"Got message {message['id']}")
                            yield AsynqMessage(message["id"], orjson.loads(message["payload"]))
                        else:
                            yield AsynqMessage(message["id"], message["payload"])
                        await cur.execute(
                            sql.SQL(
                                "DELETE FROM {table_name} WHERE id={msg_id}").format(
                                table_name=sql.Identifier(self.table_name),msg_id = sql.Literal(message["id"])
                            )
                        )
                    else:
                        return

    async def _consume_notifications_for_messages(self):
        '''
        Given a queue, consumes any new message notifications and emits them
        '''
        logging.debug(f"Listening for notifications on queue {self.queue_name}")
        async with self._db_pool.connection() as conn:
            await conn.set_autocommit(True)
            await conn.execute(
                f"LISTEN asynq_{self.queue_name}"
            )
            notify_gen =  conn.notifies()
            await anext(notify_gen)
            logging.debug(f"Got a notification on queue {self.queue_name}, resuming")
            await notify_gen.aclose()


    async def get_next_message(self, json_messages=True):
        '''
        Returns asynq messages
        '''
        # Get messages from the backlog
        while True:
            async for message in self._consume_backlog(json_messages):
                yield message
            # No more messages? Wait until we get a notification
            await self._consume_notifications_for_messages()

