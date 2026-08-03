"""
Authentication Models Package
Re-exports all models for clean imports:
    from authentication.models import User, UserProfile, AdminProfile, SocialAuth
"""
from authentication.models.user_mod import User, UserManager
from authentication.models.profile_mod import UserProfile
from authentication.models.admin_profile_mod import AdminProfile
from authentication.models.social_auth_mod import SocialAuth

__all__ = [
    "User",
    "UserManager",
    "UserProfile",
    "AdminProfile",
    "SocialAuth",
]
