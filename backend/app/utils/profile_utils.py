def calculate_profile_completion(profile) -> int:
    """
    Calculate profile completion percentage
    (based on real-world trust signals)
    """

    completion = 0

    # ===============================
    # BASIC IDENTITY
    # ===============================
    if profile.name:
        completion += 20

    if profile.email:
        completion += 20

    if profile.location:
        completion += 15

    # ===============================
    # PROFESSIONAL INFO
    # ===============================
    if profile.work:
        completion += 15

    if profile.company:
        completion += 10

    # ===============================
    # ABOUT USER
    # ===============================
    if profile.bio:
        completion += 10

    # ===============================
    # FUTURE (profile photo / KYC)
    # ===============================
    # if profile.profile_photo:
    #     completion += 10

    # Safety clamp (kabhi 100 se zyada na ho)
    return min(completion, 100)


def calculate_badge(completion_percentage: int) -> str:
    """
    Decide badge based on completion percentage
    """

    if completion_percentage >= 80:
        return "trusted"
    elif completion_percentage >= 40:
        return "verified"
    else:
        return "none"


def update_profile_trust(profile):
    """
    Update profile completion percentage and badge
    """

    completion = calculate_profile_completion(profile)
    badge = calculate_badge(completion)

    profile.completion_percentage = completion
    profile.badge = badge

    return profile
