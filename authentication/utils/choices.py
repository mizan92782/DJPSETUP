from django.db import models

class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    TENANT = "tenant", "Tenant"
    OWNER = 'owner','Owner'
    
    