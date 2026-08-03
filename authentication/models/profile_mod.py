from django.db import models
from authentication.models.user_mod import User
from phonenumber_field.modelfields import PhoneNumberField
from authentication.utils.image_path import ProfileImagePath




#! ==================== user profile =================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    dp_image = models.ImageField(upload_to=ProfileImagePath, blank=True, null=True)
    dp_image_url = models.URLField(max_length=500, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC', blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
