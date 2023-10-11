from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from API import models
from API.Schemas import Following


def create_following(db: Session, following: Following.FollowingCreate):
    result = db.execute(insert(models.Following)
                        .values(offerid=following.offerid,
                                userid=following.userid,
                                timefollowed=following.timefollowed))
    return result.first()


def delete_following(db: Session, following_id: int):
    result = db.execute(delete(models.Following).where(models.Following.id == following_id))
    return result.first()


def update_following(db: Session, following: Following.Following):
    result = db.execute(update(models.Following)
                        .where(models.Following.id == following.id)
                        .values(offerid=following.offerid,
                                userid=following.userid,
                                timefollowed=following.timefollowed))
    return result.first()


def get_following(db: Session, following_id: int):
    result = db.execute(select(models.Following).where(models.Following.id == following_id))
    return result.first()


def get_followings(db: Session, first: int, last: int):
    result = db.execute(select(models.Following).offset(first).limit(last))
    return result.all()


def get_followings_by_user(db: Session, user_id: int):
    result = db.execute(select(models.Following).where(models.Following.userid == user_id))
    return result.all()
