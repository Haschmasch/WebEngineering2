from pydantic import BaseModel

from API.models import Offer


class UserBase(BaseModel):
    email: str
    name: str
    phone_number: str


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    time_created: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserWithOffers(User):
    related_offers: list[Offer] = []

