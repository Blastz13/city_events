from typing import Dict, List

from starlette.websockets import WebSocket

# from core.db import session


class ConnectionChatManager:
    def __init__(self):
        self.active_connections: Dict[List[WebSocket]] = {}
        # self.db = session

    def is_current_user_access(self, chat_id: int, user_id: int):
        # return self.db.query(User).get(user_id) in self.db.query(ChatRoom).get(chat_id).users
        return True

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
        await websocket.accept()
        if self.is_current_user_access(chat_id, user_id):
            if chat_id not in self.active_connections.keys():
                self.active_connections[chat_id] = []
            self.active_connections[chat_id].append(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.active_connections[chat_id].remove(websocket)

    async def broadcast(self, message: dict, chat_id: int, user_id: int, websocket: WebSocket = None):
        if self.is_current_user_access(chat_id, user_id):
            for connection in self.active_connections[chat_id]:
                if websocket is not None:
                    if connection != websocket:
                        await connection.send_json(message)
                else:
                    await connection.send_json(message)
