from pydantic import BaseModel
from typing import Optional

class ChatCreate(BaseModel):
    message: str

class AdminReply(BaseModel):
    reply: str

class ChatResponse(BaseModel):
    id: int
    user_message: str
    admin_reply: Optional[str]
    status: str

    class Config:
        from_attributes = True
