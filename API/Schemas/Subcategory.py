from pydantic import BaseModel


from API.Schemas.Category import Category
from API.Schemas.Offer import Offer


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
