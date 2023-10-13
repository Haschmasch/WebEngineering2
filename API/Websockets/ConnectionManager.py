import os

from fastapi import WebSocket
from sqlalchemy.orm import Session

from API.Utils.FileOperations import read_json, write_json
from API.models import Chat
from API.Crud import Chats as ChatCrud


class ConnectionManager:

    def __init__(self, db: Session, chat_dir: str):
        self.db = db
        self.chat_dir = chat_dir
        self.offers: dict[str, list[WebSocket]] = {}
        if not os.path.exists(self.chat_dir):
            os.makedirs(self.chat_dir)

    async def connect(self, websocket: WebSocket, offerid: str):
        await websocket.accept()

        chat_db = ChatCrud.get_chat_by_offer(self.db, int(offerid))

        if not chat_db:
            new_chat = Chat.ChatCreate(offerid=int(offerid), creatorid=None)
            chat_db = ChatCrud.create_chat(self.db, new_chat)

        if offerid not in self.offers:
            self.offers[offerid] = []
        self.offers[offerid].append(websocket)

        # send previous messages to the client
        if chat_db is not None:
            chat_row = chat_db[0]
            # convert SQLAlchemy Row object to dict
            chat_dict = {column.name: getattr(chat_row, column.name) for column in chat_row.__table__.columns}
            # convert dict to Pydantic model
            chat = Chat(**chat_dict)
            message_history = self._load_message_history(chat.id)
        else:
            message_history = []
        for message in message_history:
            await websocket.send_text(message)

    async def disconnect(self, websocket: WebSocket, offerid: str):
        if offerid in self.offers and websocket in self.offers[offerid]:
            self.offers[offerid].remove(websocket)
            if not self.offers[offerid]:
                del self.offers[offerid]
        await self.broadcast(f"A user left the chat", offerid)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, offerid: str):
        chat_db = ChatCrud.get_chat_by_offer(self.db, int(offerid))
        if not chat_db:
            print("Error: Offer ID not found")
            return
        chat = Chat(**{column.name: getattr(chat_db[0], column.name) for column in chat_db[0].__table__.columns})
        # update message history in the file system
        message_history = self._load_message_history(chat.id)
        message_history.append(message)
        self._save_message_history(chat.id, message_history)

        # broadcast message to all clients in the room
        for connection in self.offers.get(offerid, []):
            await connection.send_text(message)

    def _load_message_history(self, chat_id: int):
        filename = f"{chat_id}.json"
        filepath = os.path.join(self.chat_dir, filename)
        try:
            return read_json(filepath)
        except FileNotFoundError:
            return []

    def _save_message_history(self, chat_id: int, message_history: list[str]):
        filename = f"{chat_id}.json"
        filepath = os.path.join(self.chat_dir, filename)
        write_json(filepath, message_history)
