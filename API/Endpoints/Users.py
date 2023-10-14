from API import setup_database
from API.Crud import Users
from API.Schemas import User
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=User.User, status_code=status.HTTP_201_CREATED)
def register_user(user: User.UserCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.create_user(db, user)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


# TODO: Implement proper login (maybe with jwt tokens)
@router.post("/login", response_model=User.User)
def login_user(user: User.UserLogin, db: Session = Depends(setup_database.get_db)):
    try:
        user = Users.check_user_exists(db, user)
        if user is None:
            raise HTTPException(status_code=400)
        return user
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.put("/", response_model=User.User)
def update_user(user: User.User, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.update_user(db, user)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/{user_id}", response_model=User.User)
def get_user(user_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/", response_model=list[User.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_users(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/name/{user_name}", response_model=User.User)
def get_user_by_name(user_name: str, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_user_by_name(db, user_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/{user_id}/offers", response_model=Relations.UserWithOffers)
def get_user_with_offers(user_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Users.get_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
