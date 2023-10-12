from pydantic import BaseModel


class FollowingBase(BaseModel):
    offer_id: int
    user_id: int
    time_followed: str


class FollowingCreate(FollowingBase):
    pass


class Following(FollowingBase):
    id: int

    class Config:
        from_attributes = True
