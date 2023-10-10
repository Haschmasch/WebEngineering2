from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str


class UserCreate(UserBase):
    password_hash: str


class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True


class OfferBase(BaseModel):
    title: str
    category_id: int
    subcategory_id: int
    price: float
    currency: str
    userid: int
    time_posted: str
    closed: bool
    time_closed: str
    postcode: str
    city: str
    address: str


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int
    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True


class SubcategoryBase(BaseModel):
    category_id: int
    name: str


class SubcategoryCreate(SubcategoryBase):
    pass


class Subcategory(SubcategoryBase):
    id: int
    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    offer_id: int
    creator_id: int
    time_opened: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    class Config:
        orm_mode = True


class FollowingBase(BaseModel):
    offer_id: int
    user_id: int
    time_followed: str


class FollowingCreate(FollowingBase):
    pass


class Following(FollowingBase):
    id: int
    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    chat_id: int
    client_id: int
    content: str
    timestamp: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    class Config:
        orm_mode = True



