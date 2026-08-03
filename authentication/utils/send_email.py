from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage
import datetime
from pathlib import Path
from authentication.utils.constants import APP_NAME, COMPANY_NAME
from configuration.services.email_config import get_active_email_config


def SEND_OTP_EMAIL(sub: str, email: str, otp: str) -> None:
    """
    Send OTP verification email using dynamic email configuration.
    Configuration is fetched from the database if an active EmailConfiguration exists,
    otherwise falls back to environment variables.
    """
    # Get active email configuration
    email_config = get_active_email_config()

    subject = sub
    from_email = email_config['EMAIL_HOST_USER']
    to = [email]
    logo_cid = "company_icon"

    html_content = render_to_string('otp_email.html', {
        'otp': otp,
        'year': datetime.datetime.now().year,
        'logo_cid': logo_cid,
        'app_name': APP_NAME,
        'company_name': COMPANY_NAME,
    })

    text_content = f"Your OTP is: {otp}"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    logo_path = Path(settings.BASE_DIR) / "icon.jpg"
    if logo_path.exists():
        with open(logo_path, "rb") as logo_file:
            logo = MIMEImage(logo_file.read())
            logo.add_header("Content-ID", f"<{logo_cid}>")
            logo.add_header("Content-Disposition", "inline", filename="icon.png")
            msg.attach(logo)

    msg.send(fail_silently=True)
    
