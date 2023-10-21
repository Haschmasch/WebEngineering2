"""
Schemas for the communication over the api.
Contains schemas for followings.
"""

import datetime

from pydantic import BaseModel


class FollowingBase(BaseModel):
    offer_id: int
    user_id: int
    time_followed: datetime.datetime


class FollowingCreate(FollowingBase):
    pass


class Following(FollowingBase):
    id: int

    class Config:
        from_attributes = True
