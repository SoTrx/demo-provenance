from enum import Enum

class AnnotationResult_status(str, Enum):
    Success = "success",
    Already_annotated = "already_annotated",
    Error = "error",

