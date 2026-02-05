import os
import requests

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")
FAST2SMS_URL = "https://www.fast2sms.com/dev/bulk"


def send_otp_sms(phone: str, otp: str):
    if not FAST2SMS_API_KEY:
        raise Exception("FAST2SMS API key not configured")

    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": f"Your Cyber Safe India OTP is {otp}. Do not share it with anyone.",
        "language": "english",
        "numbers": phone
    }

    response = requests.post(
        FAST2SMS_URL,
        json=payload,
        headers=headers,
        timeout=10
    )

    data = response.json()

    if not data.get("return"):
        raise Exception(f"SMS Failed: {data}")

    return data
