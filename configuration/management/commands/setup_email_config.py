from decouple import config
from django.core.management.base import BaseCommand

from ...models import EmailConfiguration


class Command(BaseCommand):
    help = "Delete existing email config rows and create one fresh config from .env"

    def handle(self, *args, **options):
        if EmailConfiguration.objects.exists():
            EmailConfiguration.objects.all().delete()

        email_config = EmailConfiguration.objects.create(
            email_host=config("EMAIL_HOST", default="smtp.gmail.com"),
            email_address=config("EMAIL_HOST_USER", default=""),
            email_password=config("EMAIL_HOST_PASSWORD", default=""),
            port=config("EMAIL_PORT", default=587, cast=int),
            use_tls=config("EMAIL_USE_TLS", default=True, cast=bool),
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Email configuration saved: "
                f"{email_config.email_address}@{email_config.email_host}:{email_config.port}"
            )
        )
        