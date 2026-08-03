from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models.user_mod import User
from authentication.models.admin_profile_mod import AdminProfile
from authentication.models.profile_mod import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.is_superuser or instance.is_staff:
        AdminProfile.objects.get_or_create(
            user=instance,
            defaults={'first_name': instance.email.split('@')[0], 'last_name': ''},
        )
    else:
        UserProfile.objects.get_or_create(user=instance)
