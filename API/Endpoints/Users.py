from API import database
from API.Crud import Users
from API.Schemas import User
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import exc
from API.setup import app


@app.post("/users/", response_model=User.User)
def register_user(user: User.UserCreate, db: Session = Depends(database.get_db())):
    try:
        return Users.create_user(db, user)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.detail)


def login_user(user: User.UserLogin, db: Session = Depends(database.get_db())):
    pass
