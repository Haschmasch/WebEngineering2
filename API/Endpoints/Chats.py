from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from API.Crud import Chats
from API.Schemas import Chat, Relations
from API.Utils.Exceptions import EntryNotFoundException
from API.Websockets.ConnectionManager import ConnectionManager
from API.setup_database import get_db
from API.Utils.ConfigManager import configuration


router = APIRouter(
    prefix="/chats",
    tags=["chats"])


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


@router.post("/", response_model=Chat.Chat, status_code=status.HTTP_201_CREATED)
def add_chat(chat: Chat.ChatCreate, db: Session = Depends(get_db)):
    try:
        return Chats.create_chat(db, chat, configuration.chat_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    try:
        Chats.delete_chat(db, chat_id, configuration.chat_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.put("/", response_model=Chat.Chat)
def update_chat(chat: Chat.Chat, db: Session = Depends(get_db)):
    try:
        return Chats.update_chat(db, chat)
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
