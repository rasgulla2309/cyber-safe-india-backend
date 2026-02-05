from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat_message import ChatMessage
from app.schemas.chat_schema import ChatCreate
from app.utils.jwt import get_current_user   # 🔐 JWT se user

router = APIRouter(prefix="/chat", tags=["User Chat"])


# =====================================================
# USER → SEND MESSAGE (AUTO GREETING SUPPORTED)
# =====================================================
@router.post("/submit")
def submit_chat(
    chat: ChatCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_text = chat.message.lower().strip()

    greetings = [
        "hi", "hello", "hey", "hii", "helloo",
        "good morning", "good evening", "good night",
        "namaste", "namaskar"
    ]

    auto_reply = None
    status = "open"

    # 🔹 auto greeting reply
    if any(greet in user_text for greet in greetings):
        auto_reply = (
            "👋 Hello! Welcome to Cyber Safe India Help Desk.\n"
            "You can ask any cyber security related question here.\n"
            "Our community team will assist you shortly."
        )

        # system reply = admin message
        system_msg = ChatMessage(
            user_id=current_user.id,
            sender="admin",
            message=auto_reply,
            status="open"
        )
        db.add(system_msg)

    # 🔹 user message
    user_msg = ChatMessage(
        user_id=current_user.id,
        sender="user",
        message=chat.message,
        status=status
    )

    db.add(user_msg)
    db.commit()

    return {
        "message": "Message sent successfully",
        "auto_reply": auto_reply
    }


# =====================================================
# USER → GET ONLY HIS CHAT
# =====================================================
@router.get("/my-chats")
def get_my_chats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    chats = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .filter(ChatMessage.status != "closed")
        .order_by(ChatMessage.created_at)
        .all()
    )

    return chats


# =====================================================
# USER → CLEAR HIS CHAT
# =====================================================
@router.put("/clear")
def clear_my_chat(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db.query(ChatMessage) \
        .filter(ChatMessage.user_id == current_user.id) \
        .update({"status": "closed"})

    db.commit()

    return {"message": "Chat cleared successfully"}
