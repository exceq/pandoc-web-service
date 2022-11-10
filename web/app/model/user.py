from datetime import datetime

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str


class UserDto(BaseModel):
    id: int
    created: datetime
    username: str

    class Config:
        orm_mode = True
