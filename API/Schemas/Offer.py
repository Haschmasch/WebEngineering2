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


class OfferCreate(OfferBase):
    user_id: int
    time_posted: str


class Offer(OfferCreate):
    id: int
    closed: bool
    time_closed: str

    class Config:
        from_attributes = True
