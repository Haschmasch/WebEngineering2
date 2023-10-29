"""
Schemas for the communication over the api.
Contains schemas for offers.
"""

import datetime
from pydantic import BaseModel, Field


class OfferBase(BaseModel):
    title: str
    category_id: int
    subcategory_id: int | None = None
    price: float | None = Field(default=None, ge=0, description="The price must be greater then zero or None instead")
    currency: str = Field(default='€', max_length=1, description="The currency of the offer")
    postcode: str
    city: str
    address: str
    description: str
    primary_image: str
    short_description: str | None = Field(default=None,
                                          description="The short description is a substring of the description")


class OfferCreate(OfferBase):
    user_id: int
    time_posted: datetime.datetime | None = None


class Offer(OfferCreate):
    id: int
    closed: bool
    time_closed: datetime.datetime | None = None

    class Config:
        from_attributes = True
