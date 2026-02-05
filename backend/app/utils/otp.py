import random
from datetime import datetime, timedelta

OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 3


def generate_otp() -> str:
    """
    Generate 6 digit numeric OTP
    """
    return str(random.randint(100000, 999999))


def get_expiry_time() -> datetime:
    """
    OTP expiry time (now + 5 minutes)
    """
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)


def is_otp_expired(expires_at: datetime) -> bool:
    """
    Check if OTP is expired
    """
    return datetime.utcnow() > expires_at
