"""
Contains all API endpoints for the '/chats' route.
"""

from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from API.Crud import Chats
from API.Schemas import Chat, Relations
from API.Utils.Exceptions import EntryNotFoundException
from API.Websockets.ConnectionManager import ConnectionManager
from API.setup_database import get_db
from API.Utils.ConfigManager import configuration
from API.Schemas.User import User
from API.Utils.Authentication import decode_and_validate_token
from typing import Annotated


router = APIRouter(
    prefix="/chats",
    tags=["chats"])

"""
Contains all API endpoints for the '/chats' route.
"""

@router.websocket("/ws/{offer_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, offer_id: str, db: Session = Depends(get_db),
                             chat_dir: str = configuration.chat_root_dir):
    manager = ConnectionManager(db, chat_dir)
    await manager.connect(websocket, offer_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{data}", websocket)
            await manager.broadcast(f"{data}", offer_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, offer_id)


"""
Endpoints for db operations on chats
"""

@router.post("/", response_model=Chat.Chat, status_code=status.HTTP_201_CREATED)
def add_chat(chat: Chat.ChatCreate, current_user: Annotated[User, Depends(decode_and_validate_token)],
             db: Session = Depends(get_db)):
    try:
        # TODO: Validate user group
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
    try:
        # TODO: Validate user group
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
    try:
        return Chats.get_chats(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offer/{offer_id}", response_model=Chat.Chat)
def get_chat_by_offer(offer_id: int, db: Session = Depends(get_db)):
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
    try:
        return Chats.get_chat_by_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
