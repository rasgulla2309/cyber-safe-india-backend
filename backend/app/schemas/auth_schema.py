from pydantic import BaseModel

# -----------------------------
# ADMIN / COMMUNITY LOGIN
# -----------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    role: str


# -----------------------------
# USER OTP LOGIN (NEW)
# -----------------------------
class OTPSendRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    phone_number: str
    otp: str

class OTPLoginResponse(BaseModel):
    access_token: str
