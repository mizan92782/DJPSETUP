import json
import random
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.db import models


def MATCH_HASED_OTP(plain_otp: str, hashed_otp: str) -> bool:
    """
    Verify OTP by comparing hash
    """
    return HASH_OTP(plain_otp) == hashed_otp

    
    
    
    
    
    
def GENERATE_OTP() -> str:
    
    return str(random.randint(100000, 999999))


def HASH_OTP(otp: str) -> str:
    """
    Hash OTP using SHA256
    """
    return hashlib.sha256(otp.encode()).hexdigest()


def VERIFY_HASH_OTP(plain_otp: str, hashed_otp: str) -> bool:
    """
    Verify OTP by comparing hash
    """
    return HASH_OTP(plain_otp) == hashed_otp


# =====================================================
# Redis Save Functions
# =====================================================
def SAVE_SIGNUP_DATA(email: str, otp: str, signup_data: dict) -> None:
    data = signup_data.copy()

    # Convert non-JSON types to string
    if "phone_number" in data and data["phone_number"] is not None:
        data["phone_number"] = str(data["phone_number"])

    data["otp"] = HASH_OTP(otp)

    cache.set(
        key=f"register:{email}",
        value=json.dumps(data),
        timeout=settings.OTP_EXPIRE_TIME,
    )

    
    
    
def save_password_forget_opt(email: str, otp: str) -> None:
    """
    Save password-forget OTP in Redis
    """
    data = {
        "otp": HASH_OTP(otp)
    }

    cache.set(
        key=f"password_forget:{email}",
        value=json.dumps(data),
        timeout=settings.OTP_EXPIRE_TIME,
    )

    