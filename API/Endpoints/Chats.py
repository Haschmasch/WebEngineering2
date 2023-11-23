"""
Contains all API endpoints for the '/chats' route.
This module handles all chat-related operations, including creating,
deleting, and fetching chats, as well as managing real-time chat connections
via WebSockets.
"""

from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from Crud import Chats
from Schemas import Chat, Relations
from Utils.Exceptions import EntryNotFoundException
from Websockets.ConnectionManager import ConnectionManager
from setup_database import get_db
from Utils.ConfigManager import configuration
from Schemas.User import User
from Utils.Authentication import decode_and_validate_token
from typing import Annotated


router = APIRouter(
    prefix="/chats",
    tags=["chats"])

"""
WebSocket Endpoints
"""

@router.websocket("/ws/{offer_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, offer_id: str, user_id: str, db: Session = Depends(get_db),
                             chat_dir: str = configuration.chat_root_dir):
    """
    Establishes a WebSocket connection for real-time chat functionality.
    :param websocket: WebSocket connection object.
    :param offer_id: ID of the offer associated with the chat.
    :param user_id: ID of the user participating in the chat.
    :param db: Database session.
    :param chat_dir: Directory to store chat logs.
    """
    manager = ConnectionManager(db, chat_dir)
    await manager.connect(websocket, offer_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{data}", offer_id, user_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, offer_id, user_id)


"""
Database Operation Endpoints for Chats
"""

@router.post("/", response_model=Chat.Chat, status_code=status.HTTP_201_CREATED)
def add_chat(chat: Chat.ChatCreate, current_user: Annotated[User, Depends(decode_and_validate_token)],
             db: Session = Depends(get_db)):
    """
    Creates a new chat in the database.
    :param chat: Chat creation schema.
    :param current_user: Currently authenticated user.
    :param db: Database session.
    :return: Created chat model.
    :raises HTTPException: 400 if the user is not authenticated or if a database error occurs,
    404 if the entry is not found.
    """
    try:
        if chat.creator_id == current_user.id:
            return Chats.create_chat(db, chat, configuration.chat_root_dir)
        raise HTTPException(status_code=400, detail="Adding a chat for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                db: Session = Depends(get_db)):
    """
    Deletes a chat from the database.
    :param chat_id: ID of the chat to be deleted.
    :param current_user: Currently authenticated user.
    :param db: Database session.
    :raises HTTPException: 400 if the user is not authenticated or if a database error occurs,
    404 if the entry is not found.
    """
    try:
        chat = Chats.get_chat(db, chat_id)
        if chat.creator_id == current_user.id:
            Chats.delete_chat(db, chat_id, configuration.chat_root_dir)
        else:
            raise HTTPException(status_code=400, detail="Deleting a chat from a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{chat_id}", response_model=Chat.Chat)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    """
    Fetches a single chat from the database by its ID.
    :param chat_id: ID of the chat to be fetched.
    :param db: Database session.
    :return: Chat model.
    :raises HTTPException: 400 if a database error occurs, 404 if the entry is not found.
    """
    try:
        return Chats.get_chat(db, chat_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Chat.Chat])
def get_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetches a list of chats from the database.
    :param skip: Number of entries to skip (for pagination).
    :param limit: Maximum number of entries to return.
    :param db: Database session.
    :return: List of chat models.
    :raises HTTPException: 400 if a database error occurs, 404 if the entry is not found.
    """
    try:
        return Chats.get_chats(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offer/{offer_id}", response_model=list[Chat.Chat])
def get_chat_by_offer(offer_id: int, db: Session = Depends(get_db)):
    """
    Fetches a chat associated with a specific offer.
    :param offer_id: ID of the offer.
    :param db: Database session.
    :return: Chat model.
    :raises HTTPException: 400 if a database error occurs, 404 if the entry is not found.
    """
    try:
        return Chats.get_chat_by_offer(db, offer_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/user/{user_id}", response_model=list[Relations.ChatWithOffer])
def get_chats_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetches all chats associated with a specific user.
    :param user_id: ID of the user.
    :param db: Database session.
    :return: List of chat models with related offers.
    :raises HTTPException: 400 if a database error occurs, 404 if the entry is not found.
    """
    try:
        return Chats.get_chat_by_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
