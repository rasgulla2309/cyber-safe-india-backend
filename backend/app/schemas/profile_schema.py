from pydantic import BaseModel, Field
from typing import Optional


# ===============================
# Profile response (self profile)
# ===============================
class ProfileResponse(BaseModel):
    id: int

    # Basic info
    name: Optional[str]
    email: Optional[str]
    bio: Optional[str]
    location: Optional[str]

    # Professional info
    work: Optional[str]
    company: Optional[str]

    # System fields
    phone_number: str
    completion_percentage: int
    badge: str

    class Config:
        from_attributes = True   # ✅ Pydantic v2


# ===============================
# Profile update request
# ===============================
class ProfileUpdateRequest(BaseModel):
    # Basic info
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=150)
    bio: Optional[str] = Field(None, max_length=300)
    location: Optional[str] = Field(None, max_length=100)

    # Professional info
    work: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=150)


# ===============================
# Public profile response
# ===============================
class PublicProfileResponse(BaseModel):
    name: Optional[str]
    work: Optional[str]
    company: Optional[str]
    phone_number: str
    badge: str
    completion_percentage: int

    class Config:
        from_attributes = True   # ✅ good practice
