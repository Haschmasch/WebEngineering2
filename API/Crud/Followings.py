import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from API import models
from API.Schemas import Following
from API.Utils.Exceptions import EntryNotFoundException


def create_following(db: Session, following: Following.FollowingCreate):
    db_following = models.Following(offer_id=following.offer_id,
                                    user_id=following.user_id,
                                    time_followed=datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    db.add(db_following)
    db.commit()
    db.refresh(db_following)
    return db_following


def delete_following(db: Session, following_id: int):
    following = get_following(db, following_id)
    if following is not None:
        db.execute(delete(models.Following).where(models.Following.id == following_id))
        db.commit()
    else:
        raise EntryNotFoundException(f"No database entry found for following_id: {following_id}")


def get_following(db: Session, following_id: int):
    result = db.scalars(select(models.Following).where(models.Following.id == following_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for following_id: {following_id}")


def get_followings(db: Session, first: int, last: int):
    result = db.scalars(select(models.Following).offset(first).limit(last))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for first: {first}, last: {last}")


def get_followings_by_user(db: Session, user_id: int):
    result = db.scalars(select(models.Following).where(models.Following.userid == user_id))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for user_id: {user_id}")
