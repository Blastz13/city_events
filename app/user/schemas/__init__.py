from .user import *


class ExceptionResponseSchema(BaseModel):
    error_code: int
    message: str
