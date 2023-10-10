from pydantic import BaseModel


class SubcategoryBase(BaseModel):
    categoryid: int
    name: str


class SubcategoryCreate(SubcategoryBase):
    pass


class Subcategory(SubcategoryBase):
    id: int
    class Config:
        orm_mode = True