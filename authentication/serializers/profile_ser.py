from rest_framework import serializers
from authentication.models.profile_mod import UserProfile
from authentication.models.admin_profile_mod import AdminProfile
import pytz


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    create_at = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'dp_image', 'create_at']
        read_only_fields = ['id', 'email', 'create_at']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'dp_image': {'required': False},
        }

    def get_create_at(self, obj):
        tz_name = obj.timezone or 'UTC'
        try:
            tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            tz = pytz.UTC
        return obj.create_at.astimezone(tz).isoformat()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.dp_image:
            request = self.context.get('request')
            url = instance.dp_image.url
            ret['dp_image'] = url if url.startswith('http') else request.build_absolute_uri(url)
        else:
            ret['dp_image'] = instance.dp_image_url or None
        return ret


class AdminProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AdminProfile
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'department', 'dp_image', 'created_at']
        read_only_fields = ['id', 'email', 'created_at']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'department': {'required': False},
            'dp_image': {'required': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.dp_image:
            request = self.context.get('request')
            url = instance.dp_image.url
            ret['dp_image'] = url if url.startswith('http') else request.build_absolute_uri(url)
        return ret
