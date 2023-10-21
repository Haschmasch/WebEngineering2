"""
Schemas for the communication over the api.
Contains schemas for jwt token communication.
"""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
