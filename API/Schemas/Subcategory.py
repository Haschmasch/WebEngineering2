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
