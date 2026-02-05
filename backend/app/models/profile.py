from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    # Relation with User
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # ===============================
    # BASIC PROFILE INFO
    # ===============================
    name = Column(String(100), nullable=True)
    email = Column(String(150), nullable=True)          # ✅ NEW
    bio = Column(String(300), nullable=True)
    location = Column(String(100), nullable=True)

    # ===============================
    # PROFESSIONAL INFO
    # ===============================
    work = Column(String(100), nullable=True)           # ✅ NEW
    company = Column(String(150), nullable=True)        # ✅ NEW

    # Phone number (copied from user for quick lookup)
    phone_number = Column(String(20), index=True, nullable=False)

    # ===============================
    # TRUST SYSTEM
    # ===============================
    completion_percentage = Column(Integer, default=0)
    badge = Column(String(20), default="none")  # none | verified | trusted

    # ===============================
    # TIMESTAMPS
    # ===============================
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ORM relation
    user = relationship("User", backref="profile", uselist=False)
