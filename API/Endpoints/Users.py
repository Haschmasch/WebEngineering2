from API import database
from API.Crud import Users
from API.Schemas import User
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends


def register_user(user: User.UserCreate, db: Session=Depends(database.get_db())):
    pass

def login_user(user: User.UserLogin, db: Session=Depends(database.get_db())):
    pass