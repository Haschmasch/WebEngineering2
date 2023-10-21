"""
Schemas for the communication over the api.
Contains schemas for subcategories.
"""

from pydantic import BaseModel


class SubcategoryBase(BaseModel):
    category_id: int
    name: str


class SubcategoryCreate(SubcategoryBase):
    pass


class Subcategory(SubcategoryBase):
    id: int

    class Config:
        from_attributes = True


