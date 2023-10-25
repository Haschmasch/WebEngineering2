"""
ConnectionManager is used to manage websocket connections
"""

from fastapi import WebSocket
from sqlalchemy.orm import Session

from API.Utils.FileOperations import read_json, write_json, get_chat_file_path
from API.models import Chat
from API.Crud import Chats as ChatCrud


class ConnectionManager:

    def __init__(self, db: Session, chat_dir: str):
        self.db = db
        self.chat_dir = chat_dir
        # Dictionary to store WebSockets associated with each offerid and user_id
        self.chats: dict[str, dict[str, WebSocket]] = {}

        #self.offers: dict[str, list[WebSocket]] = {}

    def _get_chat_db(self, offerid: str):
        """Retrieve chat from database using offer ID."""
        return ChatCrud.get_chat_by_offer(self.db, int(offerid))

    def _get_chat_from_db(self, chat_db):
        """Convert database chat object to Chat model instance."""
        return Chat(**{column.name: getattr(chat_db, column.name) for column in chat_db.__table__.columns})

    async def connect(self, websocket: WebSocket, offerid: str, userid: str):
        """Establish a WebSocket connection and retrieve previous chat messages."""
        await websocket.accept()
        chat_db = self._get_chat_db(offerid)

        # if no chat exists for the given offer ID, create one
        if not chat_db:
            new_chat = Chat.ChatCreate(offerid=int(offerid), creatorid=None)
            chat_db = ChatCrud.create_chat(self.db, new_chat, self.chat_dir)

        # retrieve and send previous messages to the connected client
        chat = self._get_chat_from_db(chat_db)
        message_history = self._load_message_history(chat.id)
        for message in message_history:
            await websocket.send_text(message)
        # store the WebSocket connection
        if offerid not in self.chats:
            self.chats[offerid] = {}
        self.chats[offerid][userid] = websocket


    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a personal message to a specific WebSocket."""
        await websocket.send_text(message)

    async def disconnect(self, websocket: WebSocket, offerid: str, userid: str):
        """Disconnect a WebSocket."""
        if offerid in self.chats and userid in self.chats[offerid]:
            del self.chats[offerid][userid]
            if not self.chats[offerid]:
                del self.chats[offerid]
        '''
        if offerid in self.offers and websocket in self.offers[offerid]:
            self.offers[offerid].remove(websocket)
            if not self.offers[offerid]:
                del self.offers[offerid]
        '''

    async def broadcast(self, message: str, offerid: str, sender_userid: str):
        """Broadcast a message to all clients associated with a specific offer ID."""
        chat_db = self._get_chat_db(offerid)
        if not chat_db:
            print("Error: Offer ID not found")
            return

        chat = self._get_chat_from_db(chat_db)
        message_history = self._load_message_history(chat.id)
        message_history.append(message)
        self._save_message_history(chat.id, message_history)
        # send the message to all clients in the room
        for userid, connection in self.chats.get(offerid, {}).items():
            if userid != sender_userid:
                await connection.send_text(message)
        '''
        for connection in self.offers.get(offerid, []):
            if connection != sender:
                await connection.send_text(message)
        '''



    def _load_message_history(self, chat_id: int):
        """Load message history for a given chat ID from a file."""
        filepath = get_chat_file_path(chat_id, self.chat_dir)
        try:
            return read_json(filepath)
        except FileNotFoundError:
            return []

    def _save_message_history(self, chat_id: int, message_history: list[str]):
        """Save message history for a given chat ID to a file."""
        filepath = get_chat_file_path(chat_id, self.chat_dir)
        write_json(filepath, message_history)

