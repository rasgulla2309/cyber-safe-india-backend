from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.scam_number import ScamNumber
from app.models.profile import Profile
from app.schemas.checker_schema import NumberCheckRequest, ReportNumberRequest
from app.services.risk_scoring import calculate_risk

router = APIRouter(
    prefix="/check",
    tags=["Number Check"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CHECK NUMBER (WITH PROFILE DATA)
@router.post("/number")
def check_number(data: NumberCheckRequest, db: Session = Depends(get_db)):

    scam = db.query(ScamNumber).filter(
        ScamNumber.phone_number == data.phone_number
    ).first()

    profile = db.query(Profile).filter(
        Profile.phone_number == data.phone_number
    ).first()

    reports = scam.report_count if scam else 0
    risk_level = calculate_risk(reports) if scam else "Safe"

    profile_data = None
    if profile:
        profile_data = {
            "name": profile.name,
            "location": profile.location,
            "bio": profile.bio,
            "badge": profile.badge,
            "completion_percentage": profile.completion_percentage
        }

    return {
        "phone_number": data.phone_number,
        "risk_level": risk_level,
        "reports": reports,
        "profile": profile_data
    }


# ✅ REPORT NUMBER
@router.post("/report")
def report_number(data: ReportNumberRequest, db: Session = Depends(get_db)):

    record = db.query(ScamNumber).filter(
        ScamNumber.phone_number == data.phone_number
    ).first()

    if record:
        record.report_count += 1
        record.scam_type = data.scam_type
    else:
        record = ScamNumber(
            phone_number=data.phone_number,
            report_count=1,
            scam_type=data.scam_type
        )
        db.add(record)

    db.commit()

    return {
        "message": "Number reported successfully",
        "phone_number": data.phone_number,
        "total_reports": record.report_count
    }
