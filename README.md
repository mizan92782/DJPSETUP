# DJPSETUP — Django Project Initial Setup

A production-ready Django REST Framework boilerplate with authentication, JWT, Celery, Redis, S3, Stripe, Swagger, and full observability stack — ready to clone and build on.

## What's Included

- **Authentication** — Custom user model, JWT login/register, OTP verification, social auth, password reset, profile management
- **Configuration** — DB-driven email config, Stripe config, certificate templates via admin
- **Celery** — Async task queue with Redis broker + django-celery-beat for scheduled tasks
- **Redis** — Auto-detected cache with graceful fallback to in-memory if Redis is unavailable
- **Storage** — Local media files in dev, AWS S3 in production (auto-detected via env vars)
- **Stripe** — Payment processing with webhook support
- **Swagger** — Interactive API docs at `/swagger/` and `/redoc/`
- **Logging** — Colored console formatter + rotating file handlers (app.log, errors.log)
- **Monitoring** — Prometheus, Grafana, Loki, Promtail, Alertmanager configs under `infra/`
- **Middleware** — Request logging, last-seen tracking, timezone detection
- **Shared Utilities** — Base model/serializer/view, custom responses, pagination, permissions, throttling, enums

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework |
| Auth | JWT (SimpleJWT), OTP, Social Auth |
| Database | SQLite (local) / PostgreSQL (production) |
| Cache / Queue | Redis 7, Celery, django-celery-beat |
| Storage | Local / AWS S3 (django-storages) |
| Payments | Stripe |
| API Docs | Swagger + ReDoc (drf-yasg) |
| Web Server | Gunicorn + Nginx |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus, Grafana, Loki, Promtail, Alertmanager |

## Project Structure

```
project/          # Django settings, urls, celery, wsgi/asgi
authentication/   # User model, register, login, OTP, social auth, profile
configuration/    # Email config, Stripe config, certificate templates (DB-driven)
stripe_config/    # Stripe setup management command
shared/           # Base classes, responses, pagination, permissions, throttling, enums
middleware/       # Request logging, last-seen middleware
logs/             # Custom log formatters and handlers
infra/            # Redis client, Celery workers, Prometheus, Grafana, Loki, Alertmanager
scripts/          # Nginx setup, seed scripts, shell helpers
templates/        # Health check page, OTP email template
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for production)

### Local Setup

```bash
git clone git@github.com:mizan92782/DJPSETUP.git
cd DJPSETUP

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Set local env
cp .env.example .env   # or create .env manually
# Set LOCAL_RUN=True in .env

python manage.py migrate
python manage.py runserver
```

### Docker Setup

```bash
# Development
docker compose -f docker-compose.dev.yml up --build

# Production
docker compose -f docker-compose.prod.yml up --build
```

API available at `http://localhost:8000`

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `LOCAL_RUN` | `True` = SQLite + local Redis, `False` = PostgreSQL + container Redis |
| `DEBUG` | Django debug mode |
| `POSTGRES_DB/USER/PASSWORD` | PostgreSQL credentials (production) |
| `REDIS_HOST/PORT/PASSWORD` | Redis connection |
| `EMAIL_HOST/PORT/USER/PASSWORD` | SMTP email settings |
| `EMAIL_BACKEND` | Email backend (console for dev, smtp for prod) |
| `USE_S3` | `True` to enable AWS S3 media storage |
| `AWS_ACCESS_KEY_ID/SECRET/BUCKET` | AWS S3 credentials |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |
| `ACCESS_TOKEN_DAYS` | JWT access token lifetime (default: 60) |
| `REFRESH_TOKEN_DAYS` | JWT refresh token lifetime (default: 60) |
| `OTP_EXPIRE_TIME` | OTP validity in seconds (default: 300) |

> **Never commit `.env` to version control.**

## Key Endpoints

| Prefix | Description |
|---|---|
| `/auth/` | Register, login, OTP, social auth, password reset, profile |
| `/settings/` | Email config, Stripe config, certificate templates |
| `/swagger/` | Swagger UI |
| `/redoc/` | ReDoc UI |
| `/health/` | Server health check with system metrics |
| `/admin/` | Django admin |

## LOCAL_RUN Flag

This project uses a `LOCAL_RUN` env flag to switch between environments automatically:

| Setting | `LOCAL_RUN=True` | `LOCAL_RUN=False` |
|---|---|---|
| Database | SQLite | PostgreSQL |
| Redis | `localhost:6380` | `redis:6379` (Docker) |
| Cache | Auto-detected Redis or in-memory | Auto-detected Redis or in-memory |
| Media | Local `media/` folder | AWS S3 (if credentials set) |
| CORS | Allow all origins | Restricted to `CORS_ALLOWED_ORIGINS` |
| SSL | Disabled | Nginx handles SSL |

## Running Tests

```bash
python manage.py test
```

## CI/CD

GitHub Actions workflow in `.github/workflows/prod-ci.yaml` runs on every push.
