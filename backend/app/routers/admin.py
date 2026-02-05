from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.models.profile import Profile
from app.schemas.chat_schema import AdminReply

router = APIRouter(prefix="/admin", tags=["Admin Panel"])


# =====================================================
# ADMIN → CHAT LIST (ONE BOX PER USER)
# Name comes from Profile table
# =====================================================
@router.get("/chats")
def get_all_chats(db: Session = Depends(get_db)):

    users = (
        db.query(
            ChatMessage.user_id,
            func.max(ChatMessage.created_at).label("last_time")
        )
        .filter(ChatMessage.status != "closed")
        .group_by(ChatMessage.user_id)
        .order_by(func.max(ChatMessage.created_at).desc())
        .all()
    )

    result = []

    for u in users:
        user = db.query(User).filter(User.id == u.user_id).first()
        profile = db.query(Profile).filter(Profile.user_id == u.user_id).first()

        if not user:
            continue

        last_msg = (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == u.user_id)
            .order_by(ChatMessage.created_at.desc())
            .first()
        )

        result.append({
            "user_id": user.id,
            # ✅ NAME FROM PROFILE (fallback handled in frontend)
            "name": profile.name if profile and profile.name else None,
            "phone_number": user.phone_number,
            "last_message": last_msg.message if last_msg else "",
            "status": last_msg.status if last_msg else "open"
        })

    return result


# =====================================================
# ADMIN → FULL CHAT OF A USER
# =====================================================
@router.get("/chat/{user_id}")
def get_user_chat(user_id: int, db: Session = Depends(get_db)):
    chats = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return chats


# =====================================================
# ADMIN → REPLY TO USER
# =====================================================
@router.put("/chat/{user_id}/reply")
def reply_chat(user_id: int, data: AdminReply, db: Session = Depends(get_db)):
    chat = ChatMessage(
        user_id=user_id,
        sender="admin",
        message=data.reply,
        status="open"
    )

    db.add(chat)
    db.commit()

    return {"message": "Reply sent successfully"}


# =====================================================
# ADMIN → MARK CHAT RESOLVED
# =====================================================
@router.put("/chat/{user_id}/resolve")
def resolve_chat(user_id: int, db: Session = Depends(get_db)):
    db.query(ChatMessage) \
        .filter(ChatMessage.user_id == user_id) \
        .update({"status": "resolved"})

    db.commit()
    return {"message": "Chat marked as resolved"}


# =====================================================
# ADMIN → CLOSE CHAT
# =====================================================
@router.put("/chat/{user_id}/close")
def close_chat(user_id: int, db: Session = Depends(get_db)):
    db.query(ChatMessage) \
        .filter(ChatMessage.user_id == user_id) \
        .update({"status": "closed"})

    db.commit()
    return {"message": "Chat closed successfully"}
