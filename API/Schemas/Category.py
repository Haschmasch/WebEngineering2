from pydantic import BaseModel
import Subcategory


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True


class CategoryWithSubcategories(Category):
    subcategories: list[Subcategory] = []

