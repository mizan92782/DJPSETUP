from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class EmailConfiguration(models.Model):
    """
    Singleton model to store email configuration settings.
    Only one instance should exist in the entire system.
    Admin can manage credentials from the admin panel or via API.
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
        verbose_name = "Email Configuration"
        verbose_name_plural = "Email Configuration"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email_address} ({self.email_host}:{self.port})"

    def save(self, *args, **kwargs):
        """Enforce singleton pattern - only one instance allowed."""
        if not self.pk and EmailConfiguration.objects.exists():
            raise ValueError("Only one email configuration instance is allowed.")
        super().save(*args, **kwargs)

    @property
    def backend(self):
        """Return the appropriate email backend."""
        return "django.core.mail.backends.smtp.EmailBackend"


class CertificateTemplate(models.Model):
    """
    Singleton model for certificate template assets.
    Only one instance is allowed in the system.
    """

    platform_icon = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    university_logo = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    signature = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    seal = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    collaborator_logo = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    certificate_template = models.FileField(upload_to='certificate_template/', null=True, blank=True)

    university_name = models.CharField(max_length=255, null=True, blank=True)
    professor_name = models.CharField(max_length=255, null=True, blank=True)
    endorser_first_designation = models.TextField(max_length=1000, null=True, blank=True)
    endorser_second_designation = models.TextField(max_length=1000, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certificate Template"
        verbose_name_plural = "Certificate Template"

    def __str__(self):
        return "Certificate Template"

    def save(self, *args, **kwargs):
        """Enforce singleton pattern - only one instance allowed."""
        if not self.pk and CertificateTemplate.objects.exists():
            raise ValueError("Only one certificate template instance is allowed.")
        super().save(*args, **kwargs)
