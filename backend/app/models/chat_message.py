from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    # kis user ka chat hai
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # message kisne bheja
    sender = Column(String, nullable=False)
    # values: "user" | "admin"

    # actual message text
    message = Column(Text, nullable=False)

    # chat status (thread-level)
    status = Column(String, default="open")
    # open | resolved | closed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
