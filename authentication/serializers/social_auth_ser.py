from rest_framework import serializers

class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(
        choices=['google', 'github', 'facebook', 'twitter', 'linkedin', 'apple'],
        required=True,
        help_text="Select OAuth provider"
    )
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=False, max_length=100, allow_blank=True, default='')
    provider_id = serializers.CharField(required=True, help_text="User ID from OAuth provider")
    dp_image = serializers.URLField(required=False, allow_null=True, allow_blank=True, default=None)
