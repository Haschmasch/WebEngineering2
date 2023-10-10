from pydantic import BaseModel


class FollowingBase(BaseModel):
    offerid: int
    userid: int
    timefollowed: str


class FollowingCreate(FollowingBase):
    pass


class Following(FollowingBase):
    id: int
    class Config:
        orm_mode = True