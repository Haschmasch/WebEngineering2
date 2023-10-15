from API import setup_database
from API.Crud import Followings
from API.Schemas import Following
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc

router = APIRouter(
    prefix="/followings",
    tags=["followings"]
)


@router.post("/", response_model=Following.Following, status_code=status.HTTP_201_CREATED)
def add_following(following: Following.FollowingCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.create_following(db, following)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.delete("/")
def delete_following(following_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        Followings.delete_following(db, following_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/{following_id}", response_model=Following.Following)
def get_following(following_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.get_following(db, following_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/", response_model=list[Following.Following])
def get_followings(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.get_followings(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/user/{user_id}", response_model=list[Relations.FollowingWithOffer])
def get_followings_with_offer(user_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Followings.get_followings_by_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
