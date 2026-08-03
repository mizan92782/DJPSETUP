"""
configuration/services/stripe_config.py — Stripe Config Service

Merged from stripe_config app.
Fetches Stripe settings from DB (singleton), falls back to environment vars.
"""
from django.conf import settings as django_settings
from django.db import DatabaseError


def get_active_stripe_config() -> dict:
    """
    Retrieve Stripe configuration from the database if it has usable values.
    Falls back to environment variables otherwise.

    Returns:
        dict: Dictionary containing Stripe configuration parameters.
    """
    try:
        from configuration.models.stripe_config_mod import StripeConfiguration
        config = StripeConfiguration.objects.first()
        if config and config.stripe_secret_key and config.stripe_publishable_key:
            return {
                'STRIPE_SECRET_KEY':      config.stripe_secret_key,
                'STRIPE_PUBLISHABLE_KEY': config.stripe_publishable_key,
                'STRIPE_WEBHOOK_SECRET':  config.stripe_webhook_secret or getattr(django_settings, 'STRIPE_WEBHOOK_SECRET', ''),
            }
    except (ImportError, DatabaseError, Exception):
        pass

    return {
        'STRIPE_SECRET_KEY':      getattr(django_settings, 'STRIPE_SECRET_KEY', ''),
        'STRIPE_PUBLISHABLE_KEY': getattr(django_settings, 'STRIPE_PUBLISHABLE_KEY', ''),
        'STRIPE_WEBHOOK_SECRET':  getattr(django_settings, 'STRIPE_WEBHOOK_SECRET', ''),
    }


def apply_stripe_config() -> None:
    """
    Applies the singleton Stripe configuration to Django settings.
    Called at startup from configuration/apps.py ready().
    Silently ignores errors during migrations.
    """
    try:
        config = get_active_stripe_config()
        django_settings.STRIPE_SECRET_KEY      = config['STRIPE_SECRET_KEY']
        django_settings.STRIPE_PUBLISHABLE_KEY = config['STRIPE_PUBLISHABLE_KEY']
        django_settings.STRIPE_WEBHOOK_SECRET  = config['STRIPE_WEBHOOK_SECRET']
    except Exception:
        pass
