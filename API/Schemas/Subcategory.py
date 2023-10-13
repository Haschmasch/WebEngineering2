from pydantic import BaseModel

from API.models import Offer, Category


class SubcategoryBase(BaseModel):
    category_id: int
    name: str


class SubcategoryCreate(SubcategoryBase):
    pass


class Subcategory(SubcategoryBase):
    id: int

    class Config:
        from_attributes = True


class SubcategoryWithOffers(Subcategory):
    related_offers: list[Offer] = []


class SubcategoryWithCategory(Subcategory):
    related_category: Category
