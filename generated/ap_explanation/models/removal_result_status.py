from enum import Enum

class RemovalResult_status(str, Enum):
    Success = "success",
    Not_found = "not_found",
    Error = "error",

