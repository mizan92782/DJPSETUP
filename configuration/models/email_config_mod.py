"""
configuration/models/email_config_mod.py — Email Configuration Model

Singleton model to store SMTP email configuration.
Admin can manage credentials from the admin panel.
Falls back to environment variables if no DB config exists.
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class EmailConfiguration(models.Model):
    """
    Singleton email configuration model.
    Only one instance should exist in the entire system.
    """
    email_host = models.CharField(
        max_length=255,
        help_text="SMTP server address (e.g., smtp.gmail.com)",
    )
    email_address = models.CharField(
        max_length=255,
        help_text="Sender email address",
    )
    email_password = models.CharField(
        max_length=255,
        help_text="SMTP password or app-specific password",
    )
    port = models.PositiveIntegerField(
        default=587,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        help_text="SMTP port (usually 587 for TLS, 465 for SSL)",
    )
    use_tls = models.BooleanField(
        default=True,
        help_text="Use TLS encryption",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'configuration'
        verbose_name = "Email Configuration"
        verbose_name_plural = "Email Configuration"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email_address} ({self.email_host}:{self.port})"

    def save(self, *args, **kwargs):
        """Enforce singleton pattern — only one instance allowed."""
        if not self.pk and EmailConfiguration.objects.exists():
            raise ValueError("Only one email configuration instance is allowed.")
        super().save(*args, **kwargs)

    @property
    def backend(self):
        """Return the appropriate email backend class path."""
        return "django.core.mail.backends.smtp.EmailBackend"
