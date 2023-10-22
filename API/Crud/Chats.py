"""
Contains all create, read, update and delete operations for chats.
"""

import datetime
from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select
from API import models
from API.Schemas import Chat
from API.Utils.FileOperations import write_json, remove_file, get_chat_file_path
from API.Utils.Exceptions import EntryNotFoundException


def create_chat(db: Session, chat: Chat.ChatCreate, chat_root_directory: str):
    db_chat = models.Chat(offer_id=chat.offer_id, creator_id=chat.creator_id,
                          time_opened=datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    try:
        filepath = get_chat_file_path(db_chat.id, chat_root_directory)
        write_json(filepath, [])
    except Exception as e:
        db.delete(db_chat)
        db.commit()
        raise Exception(f"Failed to create message history file. Error: {str(e)}")
    return db_chat


def delete_chat(db: Session, chat_id: int, chat_root_directory: str):
    chat = get_chat(db, chat_id)
    filepath = get_chat_file_path(chat_id, chat_root_directory)
    remove_file(filepath)
    if chat is not None:
        db.execute(delete(models.Chat).where(models.Chat.id == chat_id))
        db.commit()
    else:
        raise EntryNotFoundException(f"No database entry found for chat_id: {chat_id}")


def update_chat(db: Session, chat: Chat.Chat):
    result = db.scalars(
        update(models.Chat)
        .returning(models.Chat)
        .where(models.Chat.id == chat.id)
        .values(offer_id=chat.offer_id, creator_id=chat.creator_id)
    )
    db.commit()
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for chat: {chat.id}")


def get_chat(db: Session, chat_id: int):
    result = db.scalars(select(models.Chat).where(models.Chat.id == chat_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for chat_id: {chat_id}")


def get_chats(db: Session, first: int, last: int):
    result = db.scalars(select(models.Chat).offset(first).limit(last))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for first: {first}, last: {last}")


def get_chat_by_offer(db: Session, offer_id: int):
    result = db.scalars(select(models.Chat).where(models.Chat.offer_id == offer_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for offer_id: {offer_id}")


def get_chat_by_user(db: Session, user_id: int):
    result = db.scalars(select(models.Chat).where(models.Chat.creator_id == user_id))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for user_id: {user_id}")

