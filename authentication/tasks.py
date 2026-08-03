from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

@shared_task
def clear_expired_blacklist():
    expired_tokens = BlacklistedToken.objects.filter(token__is_expired=True)
    count = expired_tokens.count()
    expired_tokens.delete()
    return f"{count} expired tokens deleted"
    