from rest_framework import serializers
from authentication.models.user_mod import User


class AdminUserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    dp_image = serializers.SerializerMethodField()
    passport_public_url = serializers.SerializerMethodField()
    passed_micro_credentials = serializers.SerializerMethodField()
    enrolled_count = serializers.SerializerMethodField()
    passed_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'dp_image',
            'is_active', 'is_staff', 'is_superuser',
            'created_at',
            'enrolled_count', 'passed_count',
            'passed_micro_credentials',
            'passport_public_url',
        ]

    def get_full_name(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile:
            return f"{profile.first_name or ''} {profile.last_name or ''}".strip() or None
        return None

    def get_dp_image(self, obj):
        profile = getattr(obj, 'profile', None)
        if not profile:
            return None
        if profile.dp_image:
            request = self.context.get('request')
            url = profile.dp_image.url
            return url if url.startswith('http') else (request.build_absolute_uri(url) if request else url)
        return profile.dp_image_url or None

    def get_passport_public_url(self, obj):
        passport = getattr(obj, 'passport', None)
        return passport.public_profile_url if passport else None

    def get_passed_micro_credentials(self, obj):
        return [
            {
                'id': a.micro_credential.id,
                'credentials': a.micro_credential.credentials,
                'completed_at': a.completed_at,
            }
            for a in obj.mc_access.select_related('micro_credential').filter(status='completed')
        ]

    def get_enrolled_count(self, obj):
        return obj.mc_access.count()

    def get_passed_count(self, obj):
        return obj.mc_access.filter(status='completed').count()
