from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select
from .. import models
from ..Schemas import Chat


def create_chat(db: Session, chat: Chat.ChatCreate):
    result = db.execute(insert(models.Chat).values(offerid=chat.offerid, creatorid=chat.creatorid, timeopened=chat.timeopened))
    db.commit()
    return result.first()


def delete_chat(db: Session, chat_id: int):
    result = db.execute(delete(models.Chat).where(models.Chat.id == chat_id))
    db.commit()
    return result.first()


def update_chat(db: Session, chat: Chat.Chat):
    result = db.execute(
        update(models.Chat)
        .where(models.Chat.id == chat.id)
        .values(offerid=chat.offerid, creatorid=chat.creatorid)
    )
    db.commit()
    return result.first()


def get_chat(db: Session, chat_id: int):
    result = db.execute(select(models.Chat).where(models.Chat.id == chat_id))
    return result.first()


def get_chats(db: Session, first: int, last: int):
    result = db.execute(select(models.Chat).offset(first).limit(last))
    return result.all()


def get_chat_by_offer(db: Session, offer_id: int):
    result = db.execute(select(models.Chat).where(models.Chat.offerid == offer_id))
    return result.first()



def get_chat_by_user(db: Session, user_id: int):
    result = db.execute(select(models.Chat).where(models.Chat.creatorid == user_id))
    return result.scalars().all()

