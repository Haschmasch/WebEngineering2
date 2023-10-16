import datetime

from pydantic import BaseModel


class OfferBase(BaseModel):
    title: str
    category_id: int
    subcategory_id: int
    price: float
    currency: str
    postcode: str
    city: str
    address: str
    description: str
    primary_image: str
    description: str
    short_description: str | None = None


class OfferCreate(OfferBase):
    user_id: int
    time_posted: datetime.datetime | None = None


class Offer(OfferCreate):
    id: int
    closed: bool
    time_closed: datetime.datetime | None = None

    class Config:
        from_attributes = True
