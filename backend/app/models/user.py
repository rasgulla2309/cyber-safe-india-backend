from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Admin / Community login
    username = Column(String(50), unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=True)

    # Citizen OTP login
    phone_number = Column(String(15), unique=True, index=True, nullable=True)

    # Profile
    name = Column(String(100), nullable=True)

    profile_completion = Column(Integer, default=0)
    badge = Column(String(20), default="none")

    role = Column(String(20), default="citizen")
    # citizen | community | admin

    created_at = Column(DateTime, default=datetime.utcnow)
