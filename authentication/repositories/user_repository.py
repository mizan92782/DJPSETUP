"""
User Repository — All database query logic for the User model.

Senior pattern: Repositories are NOT instantiated (static methods).
They are the single source of truth for User DB interactions.
"""
from django.db import transaction
from django.contrib.auth import authenticate
from authentication.models.user_mod import User


class UserRepository:
    """
    Handles all database operations for the User model.
    Business logic belongs in Services, NOT here.
    """

    @staticmethod
    def get_by_email(email: str) -> User | None:
        """Fetch a user by email address."""
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        """Fetch a user by primary key."""
        return User.objects.filter(pk=user_id).first()

    @staticmethod
    def exists_by_email(email: str) -> bool:
        """Check if a user with this email exists."""
        return User.objects.filter(email=email).exists()

    @staticmethod
    def create_user(email: str, password: str) -> User:
        """Create a standard user with a hashed password."""
        return User.objects.create_user(email=email, password=password)

    @staticmethod
    def create_social_user(email: str) -> User:
        """Create a social-auth user without a usable password."""
        user = User.objects.create(email=email, is_active=True)
        user.set_unusable_password()
        user.save()
        return user

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        """Authenticate a user against the database."""
        return authenticate(email=email, password=password)

    @staticmethod
    def set_password(user: User, new_password: str) -> None:
        """Update the user's password."""
        user.set_password(new_password)
        user.save(update_fields=['password'])

    @staticmethod
    def update_last_login(user: User) -> None:
        """Manually update last_login (JWT bypasses Django's session login)."""
        from django.utils import timezone
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

    @staticmethod
    def set_active(user: User, is_active: bool) -> None:
        """Activate or deactivate a user account."""
        user.is_active = is_active
        user.save(update_fields=['is_active'])

    @staticmethod
    def list_regular_users():
        """Return queryset of all non-superuser users."""
        return User.objects.filter(is_superuser=False).select_related('profile')

    @staticmethod
    def delete_user(user: User) -> None:
        """Permanently delete a user and all related data (cascades)."""
        user.delete()
