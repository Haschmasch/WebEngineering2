from pydantic import BaseModel
import Subcategory
import Category


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


class OfferCreate(OfferBase):
    userid: int
    timeposted: str


class Offer(OfferCreate):
    id: int
    closed: bool
    timeclosed: str

    class Config:
        from_attributes = True


class OfferWithCategories(Offer):
    subcategory: Subcategory = None
    category: Category = None

