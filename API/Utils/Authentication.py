from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from API import setup_database
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from API.Schemas.JwtTokenData import TokenData
from API.Utils.ConfigManager import configuration
from API.Crud.Users import get_user_by_name
from API.Utils.Exceptions import EntryNotFoundException

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
