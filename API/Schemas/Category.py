from pydantic import BaseModel
from API.Schemas.Subcategory import Subcategory
from API.Schemas.Offer import Offer


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True


class CategoryWithSubcategories(Category):
    related_subcategories: list[Subcategory] = []


class CategoryWithOffers(Category):
    related_offers: list[Offer] = []
