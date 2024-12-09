import dataclasses
from typing import Any

@dataclasses.dataclass
class AsynqMessage:
    id: int
    message: str

@dataclasses.dataclass
class AsynqJSONMessage:
    id: int
    message: Any
