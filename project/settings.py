from pathlib import Path
from datetime import timedelta
from decouple import config
import os

try:
    import redis
except ImportError:
    redis = None

BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================
# CORE SETTINGS
# =============================================
"""
CORE SETTINGS: These are fundamental Django configurations that control the application's basic behavior.
- SECRET_KEY: Used for cryptographic signing (CSRF tokens, sessions, etc.). Must be kept secret in production.
- DEBUG: When True, shows detailed error pages. Must be False in production for security.
- ALLOWED_HOSTS: List of domain names/IPs that Django will serve. Prevents Host header attacks.
- LOCAL_RUN: Environment flag that switches between local development (SQLite, local Redis) and production (PostgreSQL, container Redis).
"""
SECRET_KEY = config("SECRET_KEY", default="django-insecure-dev-key-change-in-production")
PROJECT_NAME = config("PROJECT_NAME", default="LifeChoice API")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)

# Local vs Container Environment
LOCAL_RUN = config("LOCAL_RUN", default=False, cast=bool)
print(f"🔧 CORE SETTINGS: LOCAL_RUN={LOCAL_RUN}, DEBUG={DEBUG}")






#! =============================================
#! INSTALLED APPS
#! =============================================
"""
INSTALLED APPS: Django apps that are active in this project.
- Django Core: Admin, auth, sessions, messages, static files management.
- Third Party: REST Framework (API), Swagger (API docs), Channels (WebSockets), CORS (cross-origin requests).
- Custom Apps: Authentication app for user management.
These apps provide models, views, migrations, and admin interfaces.
"""
INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party
    "rest_framework",
    "drf_yasg",
    "phonenumber_field",
    "corsheaders",
    "django_filters",
    "django_celery_beat",

    # Your Apps
    "authentication",
    
]
print("✅ INSTALLED APPS: Loaded all Django and third-party apps")





#! =============================================
#!! =============================================
"""
MIDDLEWARE: Request/response processors that run in order for every request.
- SecurityMiddleware: Adds security headers (X-Frame-Options, etc.).
- WhiteNoiseMiddleware: Serves static files efficiently in production.
- CorsMiddleware: Handles Cross-Origin Resource Sharing (allows frontend to call API).
- SessionMiddleware: Manages user sessions.
- AuthenticationMiddleware: Attaches user info to requests.
- MessageMiddleware: Handles one-time messages (flash messages).
- CsrfViewMiddleware: Protects against Cross-Site Request Forgery attacks.
"""
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "middleware.request_log_middleware.RequestLogMiddleware",   # ✅ Colored request logging
    "middleware.last_seen_middleware.LastSeenMiddleware",       # ✅ Updates user last_seen
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
print("✅ MIDDLEWARE: Security, CORS, sessions, and authentication middleware configured")





#! =============================================
#! URL & TEMPLATES
#! =============================================
"""
URL & TEMPLATES: Configuration for URL routing and template rendering.
- ROOT_URLCONF: Main URL configuration file that routes requests to views.
- TEMPLATES: Tells Django where to find HTML templates and how to render them.
- Context processors: Functions that add variables available to all templates (e.g., user info).
"""
ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
print("✅ URL & TEMPLATES: URL routing and template configuration loaded")





#! =============================================
#!! =============================================
"""
WSGI & ASGI: Application entry points for different server types.
- WSGI (Web Server Gateway Interface): For traditional HTTP requests (REST APIs, web pages).
- ASGI (Asynchronous Server Gateway Interface): For async operations (WebSockets, real-time features).
Both are required for a full-featured Django application.
"""
WSGI_APPLICATION = "project.wsgi.application"
ASGI_APPLICATION = "project.asgi.application"
print("✅ WSGI & ASGI: Application gateways configured for HTTP and WebSocket support")


#! =============================================
#! PROXY & SECURITY SETTINGS
#! =============================================
# Trust Caddy proxy headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# SSL handled by Nginx — only enable in production
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
if LOCAL_RUN:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # Nginx handles SSL, not Django
print("🔒 PROXY & SECURITY: SSL handled by Nginx")





#! =============================================
#! PASSWORD VALIDATION
#! =============================================
"""
PASSWORD VALIDATION: Rules that enforce strong passwords when users create/change passwords.
- UserAttributeSimilarityValidator: Prevents passwords similar to username/email.
- MinimumLengthValidator: Enforces minimum 9 characters.
- CommonPasswordValidator: Blocks common passwords (e.g., "password123").
- NumericPasswordValidator: Prevents all-numeric passwords.
These validators run when users register or change passwords.
"""
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 9}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
print("✅ PASSWORD VALIDATION: Strong password rules configured (min 9 chars, no common passwords)")


#! =============================================
#! DATABASE CONFIGURATION
#! =============================================
"""
DATABASE CONFIGURATION: Switches between SQLite (local development) and PostgreSQL (production).

LOCAL_RUN=True (Development):
  - Uses SQLite: Lightweight, file-based database stored in db.sqlite3
  - No setup required, perfect for local development
  - Not suitable for production (single-user, limited concurrency)

LOCAL_RUN=False (Production):
  - Uses PostgreSQL: Robust, multi-user database running in Docker container
  - Requires POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD environment variables
  - Connects to "db" host (Docker container name) on port 5432
  - Supports multiple concurrent users and transactions
"""
if LOCAL_RUN:
    print("📊 DATABASE: Using SQLite (local development)")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    print("📊 DATABASE: Using PostgreSQL (production container)")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="life_db"),
            "USER": config("POSTGRES_USER", default="life_user"),
            "PASSWORD": config("POSTGRES_PASSWORD", default="life_password"),
            "HOST": config("DB_HOST", default="db"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }


#! =============================================
#! REDIS CONFIGURATION
#! =============================================
"""
REDIS CONFIGURATION: Sets up connection to Redis cache/message broker.

LOCAL_RUN=True (Development):
  - Connects to localhost (127.0.0.1) on port 6380
  - No password required
  - Useful for testing caching locally

LOCAL_RUN=False (Production):
  - Connects to "redis" host (Docker container name) on port 6379
  - Supports password authentication via REDIS_PASSWORD env var
  - Runs in Docker container alongside other services

The _build_redis_url() function constructs the Redis connection string with optional password.
USE_REDIS_CACHE flag auto-detects if Redis is available (with 2-second timeout).
If Redis is down, the app falls back to in-memory cache (slower but functional).
"""
if LOCAL_RUN:
    print("🔴 REDIS: Connecting to localhost:6380 (local development)")
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = config("REDIS_LOCAL_PORT", default=6380, cast=int)
    REDIS_DB = 0
    REDIS_PASSWORD = ""
else:
    print("🔴 REDIS: Connecting to redis:6379 (production container)")
    REDIS_HOST = config("REDIS_HOST", default="redis")
    REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
    REDIS_DB = config("REDIS_DB", default=0, cast=int)
    REDIS_PASSWORD = config("REDIS_PASSWORD", default="")

def _build_redis_url():
    if REDIS_PASSWORD:
        return f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    return f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

REDIS_URL = _build_redis_url()

# Auto-detect Redis availability
USE_REDIS_CACHE = False
if redis:
    try:
        r = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD or None,
            socket_connect_timeout=2,
        )
        r.ping()
        USE_REDIS_CACHE = True
        print(f"✅ REDIS: Successfully connected to {REDIS_HOST}:{REDIS_PORT}")
    except (redis.ConnectionError, Exception) as e:
        USE_REDIS_CACHE = False
        print(f"⚠️  REDIS: Connection failed, falling back to in-memory cache ({str(e)[:50]}...)")
else:
    print("⚠️  REDIS: Module not installed, using in-memory cache")


#! =============================================
# !CACHE CONFIGURATION
#! =============================================
"""
CACHE CONFIGURATION: Determines where to store cached data.

If Redis is available (USE_REDIS_CACHE=True):
  - Uses django-redis backend connected to Redis
  - Caches are shared across multiple app instances
  - Persists across app restarts
  - Ideal for production with multiple servers

If Redis is unavailable (USE_REDIS_CACHE=False):
  - Falls back to LocMemCache (in-memory cache)
  - Caches stored in application memory
  - Lost when app restarts
  - Not shared between instances
  - Suitable for single-server development

Cache is used for:
  - OTP storage during registration
  - Rate limiting counters
  - Session data
  - API response caching
"""
if USE_REDIS_CACHE:
    print("💾 CACHE: Using Redis (distributed, persistent)")
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
else:
    print("💾 CACHE: Using in-memory LocMemCache (local, non-persistent)")
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "lifechoice-local-cache",
        }
    }


#! =============================================
#! CHANNEL LAYERS (WebSocket)
#! =============================================
"""
CHANNEL LAYERS: Configuration for real-time communication (WebSockets, notifications).

If Redis is available (USE_REDIS_CACHE=True):
  - Uses channels_redis backend
  - Enables real-time messaging across multiple servers
  - Supports WebSocket connections
  - Messages persist in Redis

If Redis is unavailable (USE_REDIS_CACHE=False):
  - Falls back to InMemoryChannelLayer
  - Only works on single server
  - Messages lost on restart
  - Suitable for development

Used for:
  - Real-time notifications
  - WebSocket connections
  - Live chat/messaging
  - Server-to-client push updates
"""
if USE_REDIS_CACHE:
    print(" CHANNEL LAYERS: Using Redis (distributed WebSocket support)")
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        },
    }
else:
    print(" CHANNEL LAYERS: Using in-memory (single-server WebSocket support)")
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }


#! =============================================
#! REST FRAMEWORK
#! =============================================
"""
REST FRAMEWORK: Configuration for Django REST Framework (API framework).

Authentication:
  - JWTAuthentication: Uses JWT tokens in Authorization header (Bearer <token>)
  - Tokens are stateless (no server-side session storage needed)

Permissions:
  - AllowAny: By default, all endpoints are public
  - Specific endpoints override this with custom permission classes

Throttling (Rate Limiting):
  - AnonRateThrottle: Limits anonymous users to 100 requests/hour
  - UserRateThrottle: Limits authenticated users to 1000 requests/hour
  - Custom throttles for specific endpoints:
    * login: 5 requests/minute (prevents brute force)
    * signup: 3 requests/hour (prevents spam)
    * otp: 10 requests/hour (prevents OTP spam)
    * password_reset: 5 requests/hour (prevents abuse)
    * social_auth: 10 requests/hour (prevents OAuth spam)

These settings protect the API from abuse and ensure fair usage.
"""
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "EXCEPTION_HANDLER": "shared.responses.responses.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "login_user": "5/min",
        "login_anon": "5/min",
        "signup_user": "5/min",
        "signup_anon": "5/min",
        "otp": "10/hour",
        "password_reset": "5/hour",
        "social_auth": "10/hour",
    },
}
print(" REST FRAMEWORK: JWT authentication, public endpoints, rate limiting configured")


#! =============================================
#! SWAGGER SETTINGS
#! =============================================
"""
SWAGGER SETTINGS: Configuration for API documentation (Swagger/OpenAPI).

- SECURITY_DEFINITIONS: Defines how to authenticate in Swagger UI
  * Bearer token: Users paste JWT token in Authorization header
  * Format: "Bearer <your_jwt_token>"
- USE_SESSION_AUTH: Disabled because we use JWT, not session-based auth

Swagger UI is accessible at /api/docs/ and provides:
  - Interactive API documentation
  - Try-it-out feature to test endpoints
  - Request/response examples
  - Authentication testing
"""
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header. Example: "Bearer <token>"',
        }
    },
    "USE_SESSION_AUTH": False,
}
print(" SWAGGER: API documentation configured with JWT authentication")


#! =============================================
#! CORS SETTINGS
#! =============================================
"""
CORS SETTINGS: Cross-Origin Resource Sharing configuration.

LOCAL_RUN=True: Allows all origins (development convenience).
LOCAL_RUN=False: Restricts to specific origins from CORS_ALLOWED_ORIGINS env var.

CORS_ALLOW_CREDENTIALS=True: Allows cookies/credentials in cross-origin requests.
"""
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-timezone",
]

if LOCAL_RUN:
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]
    print(" CORS: Allow All Origins (Local)")
else:
    CORS_ALLOWED_ORIGINS = config(
        "CORS_ALLOWED_ORIGINS",
        default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost:8000,http://103.174.189.183:9913,http://3.110.127.196:9913",
        cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
    )
    CSRF_TRUSTED_ORIGINS = config(
        "CSRF_TRUSTED_ORIGINS",
        default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost:8000,http://103.174.189.183:9913,http://3.110.127.196:9913",
        cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
    )
    print(f" CORS: Restricted Origins ({len(CORS_ALLOWED_ORIGINS)} allowed)")


#! =============================================
#! JWT CONFIGURATION
#! =============================================
"""
JWT CONFIGURATION: JSON Web Token settings for authentication.

ACCESS_TOKEN: Short-lived token used for API requests
  - Lifetime: 60 days (configurable via ACCESS_TOKEN_DAYS env var)
  - Sent in Authorization header: "Bearer <access_token>"
  - Used to authenticate API requests

REFRESH_TOKEN: Long-lived token used to get new access tokens
  - Lifetime: 60 days (configurable via REFRESH_TOKEN_DAYS env var)
  - Stored securely on client (httpOnly cookie or secure storage)
  - When access token expires, client uses refresh token to get new access token

ROTATE_REFRESH_TOKENS: When True, each refresh generates a new refresh token
  - Improves security by limiting token reuse
  - Old refresh tokens become invalid

BLACKLIST_AFTER_ROTATION: When True, old tokens are blacklisted after rotation
  - Prevents token reuse attacks
  - Requires token blacklist backend (Redis or database)

AUTH_HEADER_TYPES: Specifies token format in Authorization header
  - "Bearer": Standard format "Bearer <token>"
"""
ACCESS_TOKEN_DAYS = config("ACCESS_TOKEN_DAYS", default=60, cast=int)
REFRESH_TOKEN_DAYS = config("REFRESH_TOKEN_DAYS", default=60, cast=int)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=ACCESS_TOKEN_DAYS),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_DAYS),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
print(f" JWT: Access token {ACCESS_TOKEN_DAYS} days, Refresh token {REFRESH_TOKEN_DAYS} days, rotation enabled")


#! =============================================
#! EMAIL CONFIGURATION
#! =============================================
"""
EMAIL CONFIGURATION: Settings for sending emails (OTP, password reset, notifications).

EMAIL_BACKEND: Determines how emails are sent
  - Default: console.EmailBackend (prints emails to console, for development)
  - Production: smtp.EmailBackend (sends real emails via SMTP server)

SMTP Settings (for production):
  - EMAIL_HOST: SMTP server address (e.g., smtp.gmail.com)
  - EMAIL_PORT: SMTP port (usually 587 for TLS, 465 for SSL)
  - EMAIL_USE_TLS: Enable TLS encryption
  - EMAIL_HOST_USER: SMTP username (sender email)
  - EMAIL_HOST_PASSWORD: SMTP password (app-specific password for Gmail)

OTP_EXPIRE_TIME: How long OTP codes are valid (in seconds)
  - Default: 300 seconds (5 minutes)
  - Used during registration and password reset

Email is used for:
  - OTP verification during signup
  - Password reset links
  - Account notifications
  - Email confirmations
"""
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

# OTP Settings
OTP_EXPIRE_TIME = config("OTP_EXPIRE_TIME", default=300, cast=int)
print(f" EMAIL: Backend={EMAIL_BACKEND.split('.')[-2]}, OTP expires in {OTP_EXPIRE_TIME}s")


# !=============================================
#! INTERNATIONALIZATION
#! =============================================
"""
INTERNATIONALIZATION: Settings for language and timezone support.

- USE_I18N: Enable internationalization (multi-language support)
- USE_TZ: Enable timezone support (store times in UTC, display in user's timezone)
- TIME_ZONE: Default timezone for the application (Asia/Dhaka for Bangladesh)
- LANGUAGE_CODE: Default language (en-us for English)

These settings ensure:
  - Dates/times are stored consistently in UTC
  - Displayed in user's local timezone
  - Multi-language support is available
  - Proper localization of numbers, dates, currencies
"""
USE_I18N = True
USE_TZ = True
TIME_ZONE = "Asia/Dhaka"
LANGUAGE_CODE = "en-us"
print(f" INTERNATIONALIZATION: Timezone={TIME_ZONE}, Language={LANGUAGE_CODE}, TZ support enabled")


# !=============================================
#! CUSTOM USER MODEL
# !=============================================
"""
CUSTOM USER MODEL: Tells Django to use custom User model instead of default.

AUTH_USER_MODEL = "authentication.User":
  - Uses custom User model from authentication app
  - Allows email-based authentication instead of username
  - Enables custom fields and methods

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField":
  - Uses 64-bit integer for primary keys (instead of 32-bit)
  - Supports larger datasets
  - Recommended for new projects

This must be set BEFORE creating any migrations.
"""
AUTH_USER_MODEL = "authentication.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
print(" CUSTOM USER MODEL: Using email-based authentication with BigAutoField")


# !=============================================
#! STATIC FILES
# !=============================================
"""
STATIC FILES: Configuration for CSS, JavaScript, images (non-user-uploaded files).

STATIC_URL: URL prefix for static files in browser
  - Example: /static/css/style.css

STATIC_ROOT: Directory where static files are collected for production
  - Used by "python manage.py collectstatic" command
  - Serves files via web server (nginx, Apache) in production

STATICFILES_DIRS: Additional directories to search for static files
  - Includes BASE_DIR/static if it exists

STATICFILES_STORAGE: How static files are stored/served
  - LOCAL_RUN=True: CompressedStaticFilesStorage (gzip compression for development)
  - LOCAL_RUN=False: CompressedManifestStaticFilesStorage (fingerprinting for cache busting in production)

WhiteNoise middleware serves static files efficiently without needing separate web server.
"""
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []

# WhiteNoise configuration
if LOCAL_RUN:
    print(" STATIC FILES: Using CompressedStaticFilesStorage (development)")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
else:
    print(" STATIC FILES: Using CompressedStaticFilesStorage (production)")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


#! =============================================
#! MEDIA FILES
#! =============================================
"""
MEDIA FILES: Configuration for user-uploaded files (profile pictures, documents, etc.).

LOCAL_RUN=True (Development):
  - MEDIA_URL: /media/ (URL prefix for accessing uploaded files)
  - MEDIA_ROOT: BASE_DIR/media (local directory where files are stored)
  - Files stored on local disk
  - Simple, no external dependencies

LOCAL_RUN=False (Production):
  - Attempts to use AWS S3 for cloud storage
  - Requires AWS credentials: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
  - Files stored in S3 bucket (scalable, reliable, backed up)
  - MEDIA_URL: https://bucket.s3.region.amazonaws.com/media/ (CDN URL)

FALLBACK MECHANISM:
  - If LOCAL_RUN=False but AWS credentials are missing:
    * Falls back to local file storage (MEDIA_ROOT = BASE_DIR/media)
    * Prevents app crash due to missing AWS config
    * Useful for testing production settings locally

AWS S3 Configuration:
  - AWS_S3_REGION_NAME: AWS region (default: us-east-1)
  - AWS_S3_CUSTOM_DOMAIN: Custom domain for S3 URLs
  - AWS_S3_OBJECT_PARAMETERS: Cache control headers (1 day cache)
  - DEFAULT_FILE_STORAGE: Uses custom MediaStorage backend
  - AWS_DEFAULT_ACL: None (no public access by default)
  - AWS_S3_FILE_OVERWRITE: False (don't overwrite existing files)

Media files are used for:
  - User profile pictures (dp_image)
  - Document uploads
  - Image galleries
  - Any user-generated content
"""
if LOCAL_RUN:
    print("📸 MEDIA FILES: Using local storage (BASE_DIR/media)")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    print("📸 MEDIA FILES: Attempting AWS S3 with local fallback")
    USE_S3 = config("USE_S3", default=False, cast=bool)
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")

    if USE_S3 and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
        print(" AWS S3 credentials found - using cloud storage")
        AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")
        AWS_S3_CUSTOM_DOMAIN = config(
            "AWS_S3_CUSTOM_DOMAIN",
            default=f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
        )
        AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
        AWS_DEFAULT_ACL = None
        AWS_S3_FILE_OVERWRITE = False
        DEFAULT_FILE_STORAGE = "lifechoice.storage_backends.MediaStorage"
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    else:
        print(" AWS S3 credentials missing - falling back to local storage")
        MEDIA_URL = "/media/"
        MEDIA_ROOT = BASE_DIR / "media"


#! =============================================
#! STRIPE CONFIGURATION
#! =============================================
"""
STRIPE CONFIGURATION: Payment processing settings.

STRIPE_SECRET_KEY: Private key for server-side operations
  - Used to create charges, refunds, subscriptions
  - Must be kept secret (never expose in frontend)
  - Get from Stripe Dashboard > Developers > API Keys

STRIPE_PUBLISHABLE_KEY: Public key for client-side operations
  - Used in frontend to create payment forms
  - Safe to expose in frontend code
  - Get from Stripe Dashboard > Developers > API Keys

STRIPE_WEBHOOK_SECRET: Secret for verifying webhook signatures
  - Stripe sends webhooks (payment events) to your server
  - This secret verifies webhooks are from Stripe (not forged)
  - Get from Stripe Dashboard > Developers > Webhooks

Stripe is used for:
  - Processing credit card payments
  - Subscription management
  - Refunds and chargebacks
  - Payment history and reporting

All keys should be stored in environment variables (.env file), never hardcoded.
"""
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", default="")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", default="")

SITE_BASE_URL = config("SITE_BASE_URL", default="http://localhost:8001")
PAYMENT_SUCCESS_URL = config("PAYMENT_SUCCESS_URL", default="http://localhost:3000/enrollment/success")
PAYMENT_CANCEL_URL = config("PAYMENT_CANCEL_URL", default="http://localhost:3000/enrollment/cancel")
if STRIPE_SECRET_KEY:
    print("STRIPE: Payment processing configured")
else:
    print("  STRIPE: No API keys configured - payments disabled")


#! =============================================
#! CELERY CONFIGURATION
#! =============================================
from celery.schedules import crontab

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE  # Asia/Dhaka
CELERY_ENABLE_UTC = False

# AI Question Generation
AI_ACCESS_TOKEN = config("AI_ACCESS_TOKEN", default="")

# NEW QUEUE-BASED SYSTEM - Sequential processing to prevent email blocking
# This system processes one competency at a time instead of all at once
CELERY_BEAT_SCHEDULE = {
    # OLD SYSTEM (kept for reference, disabled)
    # "auto-generate-all-questions": {
    #     "task": "questionbank.tasks.auto_generate_all_questions_task",
    #     "schedule": crontab(hour=13, minute=15),
    # },
    
    # NEW QUEUE-BASED SYSTEM - Test at 2:20 PM
    "populate-question-generation-queue": {
        "task": "questionbank.tasks.populate_generation_queue",
        "schedule": crontab(hour=17, minute=15),  # 2:40 PM - populate queue
    },
    "start-question-generation-queue": {
        "task": "questionbank.tasks.start_queue_processing",
        "schedule": crontab(hour=17, minute=20),  # 2:42 PM - start processing
    },
    
    # Keep completion email checker (still useful for legacy tracking)
    "check-completion-emails": {
        "task": "questionbank.tasks.check_and_send_completion_emails",
        "schedule": crontab(hour=18, minute=0),  # 6:00 PM daily - check and send completion emails
    },
}


print(f"⚙️  CELERY: Broker={REDIS_HOST}:{REDIS_PORT}, Timezone={CELERY_TIMEZONE}, UTC={CELERY_ENABLE_UTC}")


#! =============================================
#! LOGGING CONFIGURATION
#! =============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ── Formatters ────────────────────────────────────────────────────────
    'formatters': {
        'colored': {
            '()': 'logs.formatters.ColoredRequestFormatter',
        },
        'plain': {
            '()': 'logs.formatters.PlainRequestFormatter',
        },
    },

    # ── Handlers ──────────────────────────────────────────────────────────
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'level': 'DEBUG',
        },
        'file_app': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'app.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'plain',
            'level': 'INFO',
        },
        'file_errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'errors.log',
            'maxBytes': 5 * 1024 * 1024,   # 5 MB
            'backupCount': 10,
            'formatter': 'plain',
            'level': 'ERROR',
        },
    },

    # ── Loggers ───────────────────────────────────────────────────────────
    'loggers': {
        # API request/response logging (used by RequestLogMiddleware)
        'api.requests': {
            'handlers': ['console', 'file_app'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        # Django errors
        'django': {
            'handlers': ['console', 'file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Django database queries (only in debug mode)
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG and config('LOG_SQL', default=False, cast=bool) else 'WARNING',
            'propagate': False,
        },
        # Celery logging
        'celery': {
            'handlers': ['console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    # ── Root Logger ───────────────────────────────────────────────────────
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
print("📋 LOGGING: Configured with colored console formatter + rotating file handlers")


print("\n" + "="*60)
print("✅ SETTINGS LOADED SUCCESSFULLY")
print("="*60 + "\n")