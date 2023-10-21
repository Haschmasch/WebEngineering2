"""
Schemas for the communication over the api.
Contains schemas for categories.
"""

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
