from django.core.cache import cache
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
import json
import hashlib
import random

from authentication.models.user_mod import User
from authentication.models.profile_mod import UserProfile
from authentication.models.social_auth_mod import SocialAuth
from authentication.utils.send_email import SEND_OTP_EMAIL
from authentication.utils.constants import CACHE_REGISTER, OTP_EXPIRY_SECONDS


def generate_otp():
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))


def hash_otp(otp):
    """Hash OTP for secure storage"""
    return hashlib.sha256(otp.encode()).hexdigest()


def verify_otp(otp, hashed_otp):
    """Verify OTP against hashed version"""
    return hash_otp(otp) == hashed_otp


def save_registration_data(email, otp, data):
    """Save registration data with OTP in cache"""
    cache_key = f"{CACHE_REGISTER}:{email}"
    cache_data = {
        "otp": hash_otp(otp),
        **data
    }
    cache.set(cache_key, json.dumps(cache_data), timeout=OTP_EXPIRY_SECONDS)


def get_registration_data(email):
    """Get registration data from cache"""
    cache_key = f"{CACHE_REGISTER}:{email}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    return None


def delete_registration_data(email):
    """Delete registration data from cache"""
    cache_key = f"{CACHE_REGISTER}:{email}"
    cache.delete(cache_key)


def send_otp_email(email, otp):
    """Send OTP via email"""
    subject = "Your OTP for Registration"
    SEND_OTP_EMAIL(subject, email, otp)


def create_user_with_profile(data):
    """Create user and profile in a transaction"""
    with transaction.atomic():
        if User.objects.filter(email=data['email']).exists():
            raise Exception('An account with this email already exists.')

        user = User.objects.create_user(
            email=data['email'],
            password=data['password']
        )

        # Signal creates a blank UserProfile — update it with registration data
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.first_name = data['first_name']
        profile.last_name = data['last_name']
        profile.phone_number = data['phone_number']
        profile.save()

        return user, profile


def generate_tokens(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def authenticate_user(email, password):
    """Authenticate user with email and password"""
    user = authenticate(email=email, password=password)
    return user


def create_social_user(data):
    """Create user from social auth (Google/GitHub) without password"""
    with transaction.atomic():
        email = data['email']
        provider = data['provider']
        provider_id = data['provider_id']
        
        # Check if user already exists
        user = User.objects.filter(email=email).first()
        is_new = False
        
        if not user:
            # Create new user without password (social auth)
            user = User.objects.create(
                email=email,
                is_active=True
            )
            # Set unusable password for social auth users
            user.set_unusable_password()
            user.save()
            is_new = True
        
        # Ensure profile exists and always set names from social auth data
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.first_name = data['first_name']
        profile.last_name = data.get('last_name', '')
        profile.save(update_fields=['first_name', 'last_name'])
        
        # Create social auth record if not exists
        SocialAuth.objects.get_or_create(
            user=user,
            provider=provider,
            defaults={'provider_id': provider_id}
        )
        
        return user, profile, is_new
