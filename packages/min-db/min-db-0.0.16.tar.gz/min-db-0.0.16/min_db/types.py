from enum import Enum
from typing import Literal

from pydantic import BaseModel


class DB_TYPE(str, Enum):
    ORACLE = 'oracle'
    MYSQL = 'mysql'


class DB_INFO(BaseModel):
    type: Literal['oracle', 'mysql']
    sid: str | None
    db: str | None
    user: str
    password: str
    ip: str
    port: int
    session_pool_min: int
    session_pool_max: int

    class Config:
        extra = 'forbid'
