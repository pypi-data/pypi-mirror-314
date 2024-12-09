# PG-AsynQ

PG-AsynQ is a Python library that provides an asynchronous transaction/message queue based on PostgreSQL. 
It is inspired by [pq](https://pypi.org/project/pq/), but is built for use in asynchronous contexts such as FastAPI, 
and uses psycopg 3.x for database access.

Non blocking queuing is implemented with a combination of `LISTEN/NOTIFY` and `SKIP LOCKED`. This means that this 
library is safe to use across multiple containers/processes without duplicated processing of messages.

# How to use

1. Ensure you create the tables in [migrations](./migrations) using your preferred migration tool
2. See the [examples](./examples) for how to use the library

# Features

- [x] Create and consume queues dynamically at runtime
- [x] Consume queue from any number of consumers
- [x] Retain messages until a consumer connects
- [x] In-order processing of messages
- [ ] Message retention policies (delete older than x)