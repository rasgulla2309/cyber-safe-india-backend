from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.otp import OTP
from app.schemas.auth_schema import OTPSendRequest, OTPVerifyRequest
from app.utils.otp import generate_otp, get_expiry_time, is_otp_expired
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth/user", tags=["User Auth"])


# ======================================================
# SEND OTP (USER)
# ======================================================
@router.post("/send-otp")
def send_otp(data: OTPSendRequest, db: Session = Depends(get_db)):
    phone_number = data.phone_number.strip()

    if not phone_number or len(phone_number) < 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    # delete old OTPs
    db.query(OTP).filter(OTP.phone_number == phone_number).delete()
    db.commit()

    otp_code = generate_otp()
    expiry = get_expiry_time()

    otp_entry = OTP(
        phone_number=phone_number,
        otp_code=otp_code,
        expires_at=expiry,
        attempts=0,
        is_used=False
    )

    db.add(otp_entry)
    db.commit()

    # DEV ONLY
    print(f"[OTP] {phone_number} -> {otp_code}")

    return {"message": "OTP sent successfully"}


# ======================================================
# VERIFY OTP (USER)
# ======================================================
@router.post("/verify-otp")
def verify_otp(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    phone_number = data.phone_number.strip()
    otp = data.otp.strip()

    otp_entry = (
        db.query(OTP)
        .filter(OTP.phone_number == phone_number)
        .order_by(OTP.created_at.desc())
        .first()
    )

    if not otp_entry:
        raise HTTPException(status_code=400, detail="OTP not found")

    if otp_entry.is_used:
        raise HTTPException(status_code=400, detail="OTP already used")

    if is_otp_expired(otp_entry.expires_at):
        raise HTTPException(status_code=400, detail="OTP expired")

    if otp_entry.attempts >= 5:
        raise HTTPException(status_code=403, detail="Too many attempts")

    if otp_entry.otp_code != otp:
        otp_entry.attempts += 1
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid OTP")

    # OTP valid
    otp_entry.is_used = True
    db.commit()

    # find or create user
    user = db.query(User).filter(User.phone_number == phone_number).first()
    is_new_user = False

    if not user:
        user = User(
            phone_number=phone_number,
            role="citizen"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        is_new_user = True

    # 🔐 JWT MUST CONTAIN user_id
    token = create_access_token({
        "user_id": user.id,
        "phone_number": user.phone_number,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "is_new_user": is_new_user
    }
