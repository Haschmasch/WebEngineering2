from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from ..Utils import Hashing
from .. import models
from ..Schemas import User


def create_user(db: Session, user: User.UserCreate):
    salt = Hashing.generate_salt()
    hash_value = Hashing.generate_hash(user.password, salt)
    db_user = models.User(email=user.email, name=user.name, password_hash=hash_value,
                          password_salt=salt, phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User.User):
    result = db.execute(update(models.User)
                        .where(models.User.id == user.id)
                        .values(name=user.name, email=user.email, phone_number=user.phone_number))
    return result.first()


def update_user_password(db: Session, user_id: int, user: User.UserCreate):
    salt = Hashing.generate_salt()
    hash_value = Hashing.generate_hash(user.password, salt)
    result = db.execute(update(models.User)
                        .where(models.User.id == user_id)
                        .values(password_salt=salt, password_hash=hash_value))
    return result.first()


def get_user(db: Session, user_id: int):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    return result.first()


def get_users(db: Session, first: int, last: int):
    result = db.execute(select(models.User).offset(first).limit(last))
    return result.all()


def get_user_by_email(db: Session, email: str):
    result = db.execute(select(models.User).where(models.User.email == email))
    return result.first()


def get_user_by_name(db: Session, name: str):
    result = db.execute(select(models.User).where(models.User.name == name))
    return result.first()
