"""
Profile Repository — All database query logic for UserProfile and AdminProfile.
"""
from authentication.models.user_mod import User
from authentication.models.profile_mod import UserProfile
from authentication.models.admin_profile_mod import AdminProfile


class ProfileRepository:
    """
    Handles all database operations for user and admin profiles.
    """

    @staticmethod
    def get_or_create_user_profile(user: User) -> tuple[UserProfile, bool]:
        """Get or create a UserProfile for the given user."""
        return UserProfile.objects.get_or_create(user=user)

    @staticmethod
    def get_or_create_admin_profile(user: User, defaults: dict | None = None) -> tuple[AdminProfile, bool]:
        """Get or create an AdminProfile for the given user."""
        defaults = defaults or {
            'first_name': user.email.split('@')[0],
            'last_name': '',
        }
        return AdminProfile.objects.get_or_create(user=user, defaults=defaults)

    @staticmethod
    def update_user_profile(profile: UserProfile, **fields) -> UserProfile:
        """Update specific fields on a UserProfile."""
        for key, value in fields.items():
            setattr(profile, key, value)
        profile.save(update_fields=list(fields.keys()))
        return profile

    @staticmethod
    def update_admin_profile(profile: AdminProfile, **fields) -> AdminProfile:
        """Update specific fields on an AdminProfile."""
        for key, value in fields.items():
            setattr(profile, key, value)
        profile.save(update_fields=list(fields.keys()))
        return profile

    @staticmethod
    def get_user_profile(user: User) -> UserProfile | None:
        """Fetch UserProfile for a given user."""
        return UserProfile.objects.filter(user=user).first()

    @staticmethod
    def get_admin_profile(user: User) -> AdminProfile | None:
        """Fetch AdminProfile for a given user."""
        return AdminProfile.objects.filter(user=user).first()
