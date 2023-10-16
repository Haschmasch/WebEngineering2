from fastapi import WebSocket
from sqlalchemy.orm import Session

from API.Utils.FileOperations import read_json, write_json, get_chat_file_path
from API.models import Chat
from API.Crud import Chats as ChatCrud


class ConnectionManager:

    def __init__(self, db: Session, chat_dir: str):
        self.db = db
        self.chat_dir = chat_dir
        self.offers: dict[str, list[WebSocket]] = {}

    def _get_chat_db(self, offerid: str):
        return ChatCrud.get_chat_by_offer(self.db, int(offerid))

    def _get_chat_from_db(self, chat_db):
        return Chat(**{column.name: getattr(chat_db, column.name) for column in chat_db.__table__.columns})

    async def connect(self, websocket: WebSocket, offerid: str):
        await websocket.accept()
        chat_db = self._get_chat_db(offerid)

        if not chat_db:
            new_chat = Chat.ChatCreate(offerid=int(offerid), creatorid=None)
            chat_db = ChatCrud.create_chat(self.db, new_chat, self.chat_dir)

        self.offers.setdefault(offerid, []).append(websocket)

        # send previous messages to the client
        chat = self._get_chat_from_db(chat_db)
        message_history = self._load_message_history(chat.id)
        for message in message_history:
            await websocket.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def disconnect(self, websocket: WebSocket, offerid: str):
        if offerid in self.offers and websocket in self.offers[offerid]:
            self.offers[offerid].remove(websocket)
            if not self.offers[offerid]:
                del self.offers[offerid]
        await self.broadcast(f"A user left the chat", offerid)

    async def broadcast(self, message: str, offerid: str):
        chat_db = self._get_chat_db(offerid)
        if not chat_db:
            print("Error: Offer ID not found")
            return

        chat = self._get_chat_from_db(chat_db)
        message_history = self._load_message_history(chat.id)
        message_history.append(message)
        self._save_message_history(chat.id, message_history)

        # broadcast message to all clients in the room
        for connection in self.offers.get(offerid, []):
            await connection.send_text(message)

    def _load_message_history(self, chat_id: int):
        filepath = get_chat_file_path(chat_id, self.chat_dir)
        try:
            return read_json(filepath)
        except FileNotFoundError:
            return []

    def _save_message_history(self, chat_id: int, message_history: list[str]):
        filepath = get_chat_file_path(chat_id, self.chat_dir)
        write_json(filepath, message_history)
