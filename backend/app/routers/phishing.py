# backend/app/routers/phishing.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import SessionLocal
from app.models.scam_number import ScamNumber
from app.services.phishing_detector import analyze_url

router = APIRouter(
    prefix="/phish",
    tags=["Phishing"]
)

# ------------------------
# DATABASE
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------
# SCHEMAS
# ------------------------
class PhishCheckRequest(BaseModel):
    url: str

class PhishCheckResponse(BaseModel):
    url: str
    host: Optional[str]
    score: int
    risk_level: str
    matches: List[str]
    explain: str

class PhishReportRequest(BaseModel):
    target: str
    reason: Optional[str] = "Phishing URL"

# ------------------------
# CHECK PHISHING URL
# ------------------------
@router.post("/check", response_model=PhishCheckResponse)
def check_phish(req: PhishCheckRequest, db: Session = Depends(get_db)):

    if not req.url:
        raise HTTPException(status_code=400, detail="url required")

    # 🔥 CHECK COMMUNITY REPORTS
    record = db.query(ScamNumber).filter(
        ScamNumber.phone_number == req.url.lower()
    ).first()

    reports = record.report_count if record else 0

    # 🔥 PASS REPORT COUNT TO DETECTOR
    result = analyze_url(req.url, reports)

    return result

# ------------------------
# REPORT PHISHING URL
# ------------------------
@router.post("/report")
def report_phish(req: PhishReportRequest, db: Session = Depends(get_db)):

    target = req.target.lower().strip()
    if not target:
        raise HTTPException(status_code=400, detail="target required")

    record = db.query(ScamNumber).filter(
        ScamNumber.phone_number == target
    ).first()

    if record:
        record.report_count += 1
        record.scam_type = req.reason
    else:
        record = ScamNumber(
            phone_number=target,
            report_count=1,
            scam_type=req.reason
        )
        db.add(record)

    db.commit()

    return {
        "message": "Phishing URL reported successfully",
        "target": target,
        "total_reports": record.report_count
    }
