from pydantic import Field

from pydantic import BaseModel


class ObjectId(str):

    @classmethod
    def validate(cls, value):
        try:
            return str(value)
        except Exception as e:
            raise ValueError("Not a valid ObjectId") from e

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class MessageResponseSchema(BaseModel):
    id: ObjectId = Field(alias="_id")
    message: str = Field(..., description="message")
    user_id: int = Field(..., description="user_id")
    username: str = Field(..., description="username")
