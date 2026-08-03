from django.db import models


class StripeConfiguration(models.Model):
    """
    Singleton model to store Stripe payment configuration settings.
    Admin can manage keys from the admin panel or via API.
    """

    stripe_secret_key = models.CharField(
        max_length=255,
        help_text="Stripe secret key used for server-side operations",
    )
    stripe_publishable_key = models.CharField(
        max_length=255,
        help_text="Stripe publishable key used on the client side",
    )
    stripe_webhook_secret = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Stripe webhook signing secret (whsec_...)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stripe Configuration"
        verbose_name_plural = "Stripe Configuration"
        ordering = ["-created_at"]

    def __str__(self):
        return "Stripe Configuration"

    def save(self, *args, **kwargs):
        """Enforce singleton pattern - only one instance allowed."""
        if not self.pk and StripeConfiguration.objects.exists():
            raise ValueError("Only one stripe configuration instance is allowed.")
        super().save(*args, **kwargs)
