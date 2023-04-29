from typing import List

from sqlalchemy import select
from starlette.responses import HTMLResponse

from app.chat.schemas.schemas import MessageResponseSchema
from app.user.models import User
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from core.db import session
from core.utils import TokenHelper
from app.chat.services.consumers import ConnectionChatManager


from mongo_db import database

chat_router = APIRouter()
manager = ConnectionChatManager()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://0.0.0.0:8000/chat/ws/1/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2ODI3ODMyNzF9.2pFcqRMV23toT7FHJl0gIPtLVHt8Fq9eeBLN2_qVyQ4");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@chat_router.get("/")
async def get():
    return HTMLResponse(html)


@chat_router.websocket("/ws/{chat_id}/{client_token}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, client_token: str):
    user = TokenHelper.decode(client_token)
    db_user = await session.scalar(select(User).where(User.id == user["user_id"]))
    await manager.connect(websocket, chat_id, db_user.id)
    collection = database[str(chat_id)]
    try:
        while True:
            data = await websocket.receive_text()
            await collection.insert_one({"message": data, "user_id": db_user.id, "username": db_user.username})
            await manager.send_personal_message({"message": data,
                                                 "user_id": db_user.id,
                                                 "username": db_user.username,
                                                 "is_own_message": True,
                                                 "action": "messageChat"}, websocket)
            await manager.broadcast({"message": data,
                                     "user_id": db_user.id,
                                     "username": db_user.username,
                                     "is_own_message": False,
                                     "action": "messageChat"}, chat_id, db_user.id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)


@chat_router.get("/{chat_id}", response_model=List[MessageResponseSchema])
async def get_messages(chat_id: int):
    messages = []
    collection = database[str(chat_id)]
    async for document in collection.find().sort("_id", -1).limit(20):
        messages.append(document)
    return messages
