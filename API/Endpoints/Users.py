from datetime import timedelta
from API import setup_database
from API.Crud import Users
from API.Schemas import JwtTokenData
from API.Schemas.User import User, UserCreate
from API.Schemas import Relations
from API.Utils.Authentication import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_and_validate_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exc
from typing import Annotated

from API.Utils.Exceptions import EntryNotFoundException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.create_user(db, user)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)


# TODO: Implement proper login (maybe with jwt tokens)
@router.post("/login", response_model=JwtTokenData.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: Session = Depends(setup_database.get_db)):
    user = Users.check_user_exists(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/", response_model=User)
def update_user(user: User, current_user: Annotated[User, Depends(decode_and_validate_token)],
                db: Session = Depends(setup_database.get_db)):
    try:
        # TODO: Validate user group
        if user.id == current_user.id:
            return Users.update_user(db, user)
        raise HTTPException(status_code=400, detail="Updating a user aside from the authenticated user is not allowed.")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                db: Session = Depends(setup_database.get_db)):
    try:
        # TODO: Validate user group
        if user_id == current_user.id:
            Users.delete_user(db, user_id)
        raise HTTPException(status_code=400, detail="Deleting a user aside from the authenticated user is not allowed.")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/current", response_model=User)
def get_user(current_user: Annotated[User, Depends(decode_and_validate_token)]):
    try:
        return current_user
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_users(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/name/{user_name}", response_model=User)
def get_user_by_name(user_name: str, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_user_by_name(db, user_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offers/{user_id}/", response_model=Relations.UserWithOffers)
def get_user_with_offers(user_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
