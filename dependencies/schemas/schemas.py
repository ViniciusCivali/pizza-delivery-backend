from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attribute = True


class OrderSchema(BaseModel):
    user_id: int

    class Config:
        from_attribute = True


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attribute = True
