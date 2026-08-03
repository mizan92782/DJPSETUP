"""
Authentication Repositories Package

Repositories encapsulate all raw database query logic.
Views and Services should never write raw ORM queries — use repositories instead.
"""
from authentication.repositories.user_repository import UserRepository
from authentication.repositories.profile_repository import ProfileRepository
from authentication.repositories.social_auth_repository import SocialAuthRepository

__all__ = [
    "UserRepository",
    "ProfileRepository",
    "SocialAuthRepository",
]
