from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, or_
from API.Utils import Hashing
from API import models
from API.Schemas import User


def create_user(db: Session, user: User.UserCreate):
    salt = Hashing.generate_salt()
    hash_value = Hashing.generate_hash(user.password, salt)
    db_user = models.User(email=user.email, name=user.name, passwordhash=hash_value,
                          passwordsalt=salt, phonenumber=user.phone_number, timecreated=user.time_created)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User.User):
    result = db.scalars(update(models.User)
                        .returning(models.User)
                        .where(models.User.id == user.id)
                        .values(name=user.name, email=user.email, phonenumber=user.phone_number))
    db.commit()
    return result.first()


def update_user_password(db: Session, user_id: int, user: User.UserCreate):
    salt = Hashing.generate_salt()
    hash_value = Hashing.generate_hash(user.password, salt)
    result = db.scalars(update(models.User)
                        .returning(models.User)
                        .where(models.User.id == user_id)
                        .values(passwordsalt=salt, passwordhash=hash_value))
    db.commit()
    return result.first()


def delete_user(db: Session, user_id: int):
    db.execute(delete(models.User).where(models.User.id == user_id))
    db.commit()


def get_user(db: Session, user_id: int):
    result = db.scalars(select(models.User).where(models.User.id == user_id))
    return result.first()


def get_users(db: Session, first: int, last: int):
    result = db.scalars(select(models.User).offset(first).limit(last))
    return result.all()


def get_user_by_name(db: Session, name: str):
    result = db.scalars(select(models.User).where(models.User.name == name))
    return result.first()


def check_user_exists(db: Session, user: User.UserLogin):
    result = db.scalars(select(models.User).where(or_(models.User.email == user.email, models.User.name == user.email)))
    db_user = result.first()
    if db_user:
        hash_value = Hashing.generate_hash(user.password, db_user.salt)
        if hash_value == db_user.passwordhash:
            return db_user
    return None
