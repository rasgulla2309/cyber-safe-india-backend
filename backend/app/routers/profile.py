from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile_schema import (
    ProfileResponse,
    ProfileUpdateRequest,
    PublicProfileResponse
)
from app.utils.profile_utils import update_profile_trust
from app.utils.jwt import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


# =====================================================
# Helper function: Get or create profile
# =====================================================
def get_or_create_profile(db: Session, user: User) -> Profile:
    profile = db.query(Profile).filter(
        Profile.user_id == user.id
    ).first()

    if not profile:
        profile = Profile(
            user_id=user.id,
            phone_number=user.phone_number,
            completion_percentage=0,
            badge="none"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


# =====================================================
# GET /profile/me
# Logged-in user ka profile
# =====================================================
@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user)
    return profile


# =====================================================
# PUT /profile/me
# Logged-in user profile update
# =====================================================
@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user)

    # ===============================
    # BASIC INFO
    # ===============================
    if payload.name is not None:
        profile.name = payload.name

    if payload.email is not None:
        profile.email = payload.email

    if payload.bio is not None:
        profile.bio = payload.bio

    if payload.location is not None:
        profile.location = payload.location

    # ===============================
    # PROFESSIONAL INFO
    # ===============================
    if payload.work is not None:
        profile.work = payload.work

    if payload.company is not None:
        profile.company = payload.company

    # ===============================
    # TRUST / BADGE CALCULATION
    # ===============================
    update_profile_trust(profile)

    db.commit()
    db.refresh(profile)

    return profile


# =====================================================
# GET /profile/phone/{phone_number}
# Public profile (number search, community)
# =====================================================
@router.get(
    "/phone/{phone_number}",
    response_model=PublicProfileResponse
)
def get_public_profile(
    phone_number: str,
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.phone_number == phone_number
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile
