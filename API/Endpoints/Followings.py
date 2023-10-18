from API import setup_database
from API.Crud import Followings
from API.Schemas import Following
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc
from API.Utils.Exceptions import EntryNotFoundException
from API.Schemas.User import User
from API.Utils.Authentication import decode_and_validate_token
from typing import Annotated


router = APIRouter(
    prefix="/followings",
    tags=["followings"]
)


@router.post("/", response_model=Following.Following, status_code=status.HTTP_201_CREATED)
def add_following(following: Following.FollowingCreate, current_user: Annotated[User, Depends(decode_and_validate_token)],
                  db: Session = Depends(setup_database.get_db)):
    try:
        # TODO: Validate user group
        if following.user_id == current_user.id:
            return Followings.create_following(db, following)
        raise HTTPException(status_code=400, detail="Adding a following for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_following(following_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                     db: Session = Depends(setup_database.get_db)):
    try:
        # TODO: Validate user group
        following = Followings.get_following(db, following_id)
        if following.user_id == current_user.id:
            Followings.delete_following(db, following_id)
        raise HTTPException(status_code=400, detail="Deleting a following for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{following_id}", response_model=Relations.FollowingWithOffer)
def get_following(following_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.get_following(db, following_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Relations.FollowingWithOffer])
def get_followings(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.get_followings(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/user/{user_id}", response_model=list[Relations.FollowingWithOffer])
def get_followings_by_user(user_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.get_followings_by_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
