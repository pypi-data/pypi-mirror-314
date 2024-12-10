from enum import Enum
from typing import Any, Dict, TypedDict


class Status(str, Enum):
    SUCCESS = 'Success'
    FAILED = 'Failed'


class ApiResponse(TypedDict):
    status: Status
    data: Dict[str, Any]
