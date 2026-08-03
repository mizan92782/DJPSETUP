from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?\d+$',
    message="Phone number must contain only digits"
)
