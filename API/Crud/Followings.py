import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from API import models
from API.Schemas import Following


def create_following(db: Session, following: Following.FollowingCreate):
    db_following = models.Following(offer_id=following.offer_id,
                                    user_id=following.user_id,
                                    time_followed=datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    db.add(db_following)
    db.commit()
    db.refresh(db_following)
    return db_following


def delete_following(db: Session, following_id: int):
    db.execute(delete(models.Following).where(models.Following.id == following_id))
    db.commit()


def get_following(db: Session, following_id: int):
    result = db.scalars(select(models.Following).where(models.Following.id == following_id))
    return result.first()


def get_followings(db: Session, first: int, last: int):
    result = db.scalars(select(models.Following).offset(first).limit(last))
    return result.all()


def get_followings_by_user(db: Session, user_id: int):
    result = db.scalars(select(models.Following).where(models.Following.userid == user_id))
    return result.all()
