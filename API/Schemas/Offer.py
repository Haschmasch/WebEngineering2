from pydantic import BaseModel


class OfferBase(BaseModel):
    title: str
    category_id: int
    subcategory_id: int
    price: float
    currency: str
    userid: int
    timeposted: str
    closed: bool
    timeclosed: str
    postcode: str
    city: str
    address: str


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int
    class Config:
        orm_mode = True