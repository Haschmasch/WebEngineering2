"""
Contains all create, read, update and delete operations for users.
"""

import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, or_
from API.Utils import Hashing
from API import models
from API.Schemas import User
from API.Utils.Exceptions import EntryNotFoundException


def create_user(db: Session, user: User.UserCreate):
    salt = Hashing.generate_salt()
    hash_value = Hashing.generate_hash(user.password, salt)
    db_user = models.User(email=user.email, name=user.name, password_hash=hash_value,
                          password_salt=salt, phone_number=user.phone_number,
                          time_created=datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user is not None:
        db.execute(delete(models.User).where(models.User.id == user_id))
        db.commit()
    else:
        raise EntryNotFoundException(f"No database entry found for user_id: {user_id}")


def update_user(db: Session, user: User.User):
    result = db.scalars(update(models.User)
                        .returning(models.User)
                        .where(models.User.id == user.id)
                        .values(name=user.name, email=user.email, phone_number=user.phone_number))
    db.commit()
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for user: {user.id}")


def update_user_password(db: Session, user_id: int, user: User.UserCreate):
    salt = Hashing.generate_salt()
    hash_value = Hashing.generate_hash(user.password, salt)
    result = db.scalars(update(models.User)
                        .returning(models.User)
                        .where(models.User.id == user_id)
                        .values(password_salt=salt, password_hash=hash_value))
    db.commit()
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for user_id: {user_id}")


def get_user(db: Session, user_id: int):
    result = db.scalars(select(models.User).where(models.User.id == user_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for user_id: {user_id}")


def get_users(db: Session, first: int, last: int):
    result = db.scalars(select(models.User).offset(first).limit(last))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for first: {first}, last: {last}")


def get_user_by_name(db: Session, name: str):
    result = db.scalars(select(models.User).where(models.User.name == name))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for name: {name}")


def check_user_exists(db: Session, username: str, password: str):
    # This checks both the name and the email-address of the user, since both are unique in the database,
    # so the user can login with either. The variable name 'username' comes from the OAuth2 specification.
    result = db.scalars(select(models.User).where(or_(models.User.name == username, models.User.email == username)))
    db_user = result.first()
    if db_user:
        hash_value = Hashing.generate_hash(password, db_user.password_salt)
        if hash_value == db_user.password_hash:
            return db_user
    return None
