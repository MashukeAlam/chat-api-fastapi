from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from schemas import User, Message
import crud
from typing import List
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebSocketManager:
    def __init__(self):
        self.connections: List[WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.connections[username] = websocket

    def disconnect(self, username: str):
        if username in self.connections:
            del self.connections[username]

    async def send_message(self, receiver: str, message: str):
        if receiver in self.connections:
            await self.connections[receiver].send_text(message)
        else:
            print(f"User {receiver} not connected")

manager = WebSocketManager()

@app.post("/users/")
def create_user(user: User):
    if crud.get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    crud.create_user(user)
    return {"message": "User created successfully"}

@app.post("/messages/")
def send_message(message: Message):
    if not crud.get_user(message.sender) or not crud.get_user(message.receiver):
        raise HTTPException(status_code=404, detail="User not found")
    crud.send_message(message)
    return {"message": "Message sent successfully"}

@app.get("/messages/{sender}/{receiver}")
def get_chat_history(sender: str, receiver: str):
    messages = crud.get_messages(sender, receiver)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")

    return {"messages": messages}

@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    if not crud.get_user(username):
        await websocket.close()
        return

    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming message
            # Format: {"receiver": "username", "content": "message"}
            message_data = json.loads(data)
            receiver = message_data.get("receiver")
            content = message_data.get("content")

            if not crud.get_user(receiver):
                await websocket.send_text(json.dumps({"error": "Receiver not found"}))
                continue

            # Save message to database
            message = Message(sender=username, receiver=receiver, content=content)
            crud.send_message(message)

            # Broadcast message to the receiver
            await manager.send_message(receiver, json.dumps({"sender": username, "content": content}))

    except WebSocketDisconnect:
        manager.disconnect(username)

# Run with: uvicorn websocket_server:app --reload