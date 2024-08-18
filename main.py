from fastapi import FastAPI, HTTPException
from schemas import User, Message
import crud

app = FastAPI()

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
    print(messages)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")

    return {"messages": messages}
