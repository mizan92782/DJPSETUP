"""
Service module for fetching email configuration from the database.
Singleton pattern: only one EmailConfiguration exists.
Falls back to environment variables if no configuration exists.
"""

from django.conf import settings as django_settings
from django.db import DatabaseError


def get_active_email_config():
    """
    Retrieves the singleton email configuration from the database.
    Falls back to environment variables if no configuration exists or DB is unavailable.

    Returns:
        dict: Dictionary containing email configuration parameters.
    """
    try:
        from ..models import EmailConfiguration
        config = EmailConfiguration.objects.first()

        if config:
            return {
                'EMAIL_BACKEND': getattr(config, 'backend', 'django.core.mail.backends.smtp.EmailBackend'),
                'EMAIL_HOST': config.email_host,
                'EMAIL_PORT': config.port,
                'EMAIL_USE_TLS': config.use_tls,
                'EMAIL_USE_SSL': getattr(config, 'use_ssl', False),
                'EMAIL_HOST_USER': config.email_address,
                'EMAIL_HOST_PASSWORD': config.email_password,
            }
    except (ImportError, DatabaseError, Exception):
        pass

    # Fallback to environment variables
    return {
        'EMAIL_BACKEND': django_settings.EMAIL_BACKEND,
        'EMAIL_HOST': django_settings.EMAIL_HOST,
        'EMAIL_PORT': django_settings.EMAIL_PORT,
        'EMAIL_USE_TLS': django_settings.EMAIL_USE_TLS,
        'EMAIL_USE_SSL': getattr(django_settings, 'EMAIL_USE_SSL', False),
        'EMAIL_HOST_USER': django_settings.EMAIL_HOST_USER,
        'EMAIL_HOST_PASSWORD': django_settings.EMAIL_HOST_PASSWORD,
    }


def apply_email_config():
    """
    Applies the singleton email configuration to Django settings.
    Called at startup to override env-based settings with DB values.
    Silently ignores errors during migrations.
    """
    try:
        config = get_active_email_config()

        django_settings.EMAIL_BACKEND = config['EMAIL_BACKEND']
        django_settings.EMAIL_HOST = config['EMAIL_HOST']
        django_settings.EMAIL_PORT = config['EMAIL_PORT']
        django_settings.EMAIL_USE_TLS = config['EMAIL_USE_TLS']
        django_settings.EMAIL_USE_SSL = config['EMAIL_USE_SSL']
        django_settings.EMAIL_HOST_USER = config['EMAIL_HOST_USER']
        django_settings.EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
    except Exception:
        pass
