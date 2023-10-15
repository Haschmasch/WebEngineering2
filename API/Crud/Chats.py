import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select
from API import models
from API.Schemas import Chat


def create_chat(db: Session, chat: Chat.ChatCreate):
    db_chat = models.Chat(offer_id=chat.offer_id, creator_id=chat.creator_id,
                          time_opened=datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def delete_chat(db: Session, chat_id: int):
    result = db.execute(delete(models.Chat).where(models.Chat.id == chat_id))
    db.commit()
    return result.first()


def update_chat(db: Session, chat: Chat.Chat):
    result = db.scalars(
        update(models.Chat)
        .returning(models.Chat)
        .where(models.Chat.id == chat.id)
        .values(offer_id=chat.offer_id, creator_id=chat.creator_id)
    )
    db.commit()
    return result.first()


def get_chat(db: Session, chat_id: int):
    result = db.scalars(select(models.Chat).where(models.Chat.id == chat_id))
    return result.first()


def get_chats(db: Session, first: int, last: int):
    result = db.scalars(select(models.Chat).offset(first).limit(last))
    return result.all()


def get_chat_by_offer(db: Session, offer_id: int):
    result = db.scalars(select(models.Chat).where(models.Chat.offer_id == offer_id))
    return result.first()


def get_chat_by_user(db: Session, user_id: int):
    result = db.scalars(select(models.Chat).where(models.Chat.creator_id == user_id))
    return result.all()

