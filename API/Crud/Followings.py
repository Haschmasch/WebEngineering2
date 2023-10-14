from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from API import models
from API.Schemas import Following


def create_following(db: Session, following: Following.FollowingCreate):
    db_following = models.Following(offerid=following.offer_id,
                                    userid=following.user_id,
                                    timefollowed=following.time_followed)
    db.add(db_following)
    db.commit()
    db.refresh(db_following)
    return db_following


def delete_following(db: Session, following_id: int):
    result = db.execute(delete(models.Following).where(models.Following.id == following_id))
    db.commit()
    return result.first()


def update_following(db: Session, following: Following.Following):
    result = db.execute(update(models.Following)
                        .where(models.Following.id == following.id)
                        .values(offerid=following.offer_id,
                                userid=following.user_id,
                                timefollowed=following.time_followed))
    db.commit()
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
