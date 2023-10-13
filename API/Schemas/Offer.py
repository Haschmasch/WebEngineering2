from pydantic import BaseModel
from API.Schemas.Subcategory import Subcategory
from API.Schemas.Category import Category
from API.models import User


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


class OfferWithRelations(Offer):
    related_subcategory: Subcategory = None
    related_category: Category = None
    related_user: User = None

