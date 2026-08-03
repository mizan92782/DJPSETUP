from django.db import models
from django.utils import timezone
from authentication.models.user_mod import User


class SocialAuth(models.Model):
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('github', 'GitHub'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('apple', 'Apple'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_auth')
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    provider_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('provider', 'provider_id')
    
    def __str__(self):
        return f"{self.user.email} - {self.provider}"
