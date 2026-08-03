from django.db import models
from django.utils import timezone
from authentication.models.user_mod import User
from authentication.utils.image_path import ProfileImagePath


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    dp_image = models.ImageField(upload_to=ProfileImagePath, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.email}"
