"""
Social Auth Repository — All database query logic for the SocialAuth model.
"""
from authentication.models.user_mod import User
from authentication.models.social_auth_mod import SocialAuth


class SocialAuthRepository:
    """
    Handles all database operations for social authentication records.
    """

    @staticmethod
    def get_by_provider(provider: str, provider_id: str) -> SocialAuth | None:
        """Fetch a SocialAuth record by provider and provider_id."""
        return SocialAuth.objects.filter(provider=provider, provider_id=provider_id).first()

    @staticmethod
    def get_or_create(user: User, provider: str, provider_id: str) -> tuple[SocialAuth, bool]:
        """Get or create a social auth record linking user to provider."""
        return SocialAuth.objects.get_or_create(
            user=user,
            provider=provider,
            defaults={'provider_id': provider_id},
        )

    @staticmethod
    def user_has_provider(user: User, provider: str) -> bool:
        """Check if a user already has a social auth record for this provider."""
        return SocialAuth.objects.filter(user=user, provider=provider).exists()
