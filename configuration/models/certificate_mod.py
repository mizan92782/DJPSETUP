"""
configuration/models/certificate_mod.py — Certificate Template Model

Singleton model for certificate template assets.
Only one instance is allowed in the system.
"""
from django.db import models


class CertificateTemplate(models.Model):
    """
    Singleton certificate template model.
    Stores logo, signature, seal, and template file assets.
    """
    platform_icon         = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    university_logo       = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    signature             = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    seal                  = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    collaborator_logo     = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    certificate_template  = models.FileField(upload_to='certificate_template/', null=True, blank=True)
    university_name       = models.CharField(max_length=255, null=True, blank=True)
    professor_name        = models.CharField(max_length=255, null=True, blank=True)
    endorser_first_designation  = models.TextField(max_length=1000, null=True, blank=True)
    endorser_second_designation = models.TextField(max_length=1000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'configuration'
        verbose_name = "Certificate Template"
        verbose_name_plural = "Certificate Template"

    def __str__(self):
        return "Certificate Template"

    def save(self, *args, **kwargs):
        """Enforce singleton pattern — only one instance allowed."""
        if not self.pk and CertificateTemplate.objects.exists():
            raise ValueError("Only one certificate template instance is allowed.")
        super().save(*args, **kwargs)
