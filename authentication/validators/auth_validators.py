"""
Authentication Validators — Custom field validators for auth-related inputs.

Used in serializers and service layer validation.
All validators follow Django/DRF's validator protocol:
  raise serializers.ValidationError on failure.
"""
import re
from rest_framework import serializers


class PasswordStrengthValidator:
    """
    Validates that a password meets security requirements:
    - Minimum 9 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """

    def __call__(self, value: str) -> None:
        errors = []
        if len(value) < 9:
            errors.append("Password must be at least 9 characters long.")
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            errors.append("Password must contain at least one special character.")
        if errors:
            raise serializers.ValidationError(errors)


class EmailValidator:
    """
    Validates that an email is properly formatted and not from a disposable domain.
    """

    BLOCKED_DOMAINS = {
        'mailinator.com', 'tempmail.com', 'throwaway.email',
        'guerrillamail.com', 'yopmail.com', 'sharklasers.com',
    }

    def __call__(self, value: str) -> None:
        value = value.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid email address.")
        domain = value.split('@')[-1]
        if domain in self.BLOCKED_DOMAINS:
            raise serializers.ValidationError("Registration with disposable email addresses is not allowed.")


class PhoneNumberValidator:
    """
    Validates that a phone number is in a valid international format.
    Accepts: +880XXXXXXXXXX, +1XXXXXXXXXX, etc.
    """

    def __call__(self, value: str) -> None:
        pattern = r'^\+?[1-9]\d{6,14}$'
        if not re.match(pattern, str(value)):
            raise serializers.ValidationError(
                "Enter a valid phone number in international format (e.g., +8801XXXXXXXXX)."
            )


class OTPValidator:
    """
    Validates that an OTP is exactly 6 numeric digits.
    """

    def __call__(self, value: str) -> None:
        if not re.match(r'^\d{6}$', str(value)):
            raise serializers.ValidationError("OTP must be a 6-digit numeric code.")


# ─── Standalone validator functions (for use in serializer field definitions) ──

def validate_password_strength(value: str) -> str:
    """Functional validator for password strength. Returns value if valid."""
    PasswordStrengthValidator()(value)
    return value


def validate_otp_format(value: str) -> str:
    """Functional validator for OTP format. Returns value if valid."""
    OTPValidator()(value)
    return value
