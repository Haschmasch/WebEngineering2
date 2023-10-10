from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    phone_number: str


class UserCreate(UserBase):
    password: str
    timecreated: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

