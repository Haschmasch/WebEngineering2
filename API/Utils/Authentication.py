"""
Utilities for authentication using JWT bearer tokens.
Follows the OAuth2 standard, since it is supported by the fastapi framework.
"""

from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
import setup_database
from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from Schemas.JwtTokenData import TokenData
from Utils.ConfigManager import configuration
from Crud.Users import get_user_by_name
from Utils.Exceptions import EntryNotFoundException

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360

# The tokenUrl specifies the api endpoint where the token can be created with the user credentials
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    This funtion creates a new jwt token based on the passed data.
    :param data: The data to be encoded
    :param expires_delta: The expiration time delta.
    :return: The encoded jwt token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, configuration.jwt_secret, ALGORITHM)
    return encoded_jwt


def decode_and_validate_token(token: Annotated[str, Depends(oauth2_scheme)],
                              db: Session = Depends(setup_database.get_db)):
    """
    Decodes and validates the jwt token. Raises an error, of the token could not be validated.
    :param token: The jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: The user model that was evaluated by reading the jwt sub
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, configuration.jwt_secret, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    try:
        user = get_user_by_name(db, token_data.username)
    except EntryNotFoundException:
        raise credentials_exception
    return user
