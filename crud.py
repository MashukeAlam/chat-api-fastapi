from database import users_collection, messages_collection
from schemas import User, Message
from datetime import datetime

def serialize_message(message):
    return {
        **message,
        "_id": str(message["_id"]),
        "timestamp": message["timestamp"].isoformat() if isinstance(message["timestamp"], datetime) else message["timestamp"]
    }

# User-related operations
def create_user(user: User):
    users_collection.insert_one(user.dict())

def get_user(username: str):
    user_data = users_collection.find_one({"username": username})
    return User(**user_data) if user_data else None

# Message-related operations
def send_message(message: Message):
    message.timestamp = datetime.utcnow()
    messages_collection.insert_one(message.dict())

def get_messages(sender: str, receiver: str):
    messages = messages_collection.find({
        "$or": [
            {"sender": sender, "receiver": receiver},
            {"sender": receiver, "receiver": sender}
        ]
    })

    return [serialize_message(message) for message in messages]

