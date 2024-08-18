from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str

class Message(BaseModel):
    sender: str
    receiver: str
    content: str
    timestamp: Optional[datetime] = None
