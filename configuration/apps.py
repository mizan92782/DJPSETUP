from django.apps import AppConfig


class ConfigurationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configuration'

    def ready(self):
        """
        Apply email and Stripe configuration from database when app starts.
        This overrides environment variables with database settings if active configs exist.
        """
        # Apply email config
        try:
            from configuration.services.email_config import apply_email_config
            apply_email_config()
        except Exception as e:
            print(f"⚠️  CONFIGURATION: Could not apply email config — {e}")

        # Apply Stripe config
        try:
            from configuration.services.stripe_config import apply_stripe_config
            apply_stripe_config()
        except Exception as e:
            print(f"⚠️  CONFIGURATION: Could not apply Stripe config — {e}")
