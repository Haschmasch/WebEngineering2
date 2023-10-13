from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session

from API.Websockets.ConnectionManager import ConnectionManager
from API.database import get_db
from API.Utils.ConfigManager import ConfigManager


#TODO: instantiate ConfigManager as a singleton avoiding circular imports (database.py <> setup.py)
config_manager = ConfigManager()
router = APIRouter()


@router.websocket("/ws/{offerid}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, offerid: str, db: Session = Depends(get_db), chat_dir: str = config_manager.chat_root_dir):
    manager = ConnectionManager(db, chat_dir)
    await manager.connect(websocket, offerid)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{data}", websocket)
            await manager.broadcast(f"{data}", offerid)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, offerid)
