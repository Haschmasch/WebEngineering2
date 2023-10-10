from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str


class UserCreate(UserBase):
    password_hash: str


class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True