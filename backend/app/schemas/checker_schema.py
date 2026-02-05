from pydantic import BaseModel


class NumberCheckRequest(BaseModel):
    phone_number: str


class ReportNumberRequest(BaseModel):
    phone_number: str
    scam_type: str
