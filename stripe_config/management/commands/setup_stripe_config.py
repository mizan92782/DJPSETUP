from decouple import config
from django.core.management.base import BaseCommand

from ...models import StripeConfiguration


class Command(BaseCommand):
    help = "Delete existing Stripe config and create fresh config from .env"

    def handle(self, *args, **options):
        if StripeConfiguration.objects.exists():
            StripeConfiguration.objects.all().delete()
            self.stdout.write(self.style.WARNING("Old Stripe configuration deleted."))

        stripe_config = StripeConfiguration.objects.create(
            stripe_secret_key=config("STRIPE_SECRET_KEY", default=""),
            stripe_publishable_key=config("STRIPE_PUBLISHABLE_KEY", default=""),
            stripe_webhook_secret=config("STRIPE_WEBHOOK_SECRET", default=""),
        )

        self.stdout.write(self.style.SUCCESS(
            f"✅ Stripe configuration created:\n"
            f"   Publishable Key : {stripe_config.stripe_publishable_key[:12]}...\n"
            f"   Secret Key      : {stripe_config.stripe_secret_key[:12]}...\n"
            f"   Webhook Secret  : {stripe_config.stripe_webhook_secret[:12] or 'not set'}..."
        ))
