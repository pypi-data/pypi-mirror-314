from typing import TypeVar
from enum import Enum


T = TypeVar('T')

class ExecType(Enum):
    send = "send"
    fetchone = "fetchone"
    fetchall = "fetchall"





