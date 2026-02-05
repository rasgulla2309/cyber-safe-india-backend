from sqlalchemy import Column, Integer, String
from app.database import Base

class ScamNumber(Base):
    __tablename__ = "scam_numbers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    report_count = Column(Integer, default=0)
    scam_type = Column(String, default="Unknown")
