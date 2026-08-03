from django.apps import AppConfig


class StripeConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe_config"

    def ready(self):
        """
        Apply Stripe configuration from database when app starts.
        This overrides environment variables with database settings if an active config exists.
        """
        try:
            from .services.stripe_config import apply_stripe_config

            apply_stripe_config()
        except Exception as e:
            # During migrations, the table may not exist yet - that's okay
            # Log but don't crash the app
            print(f"⚠️  STRIPE CONFIG: Could not apply config - {e}")
