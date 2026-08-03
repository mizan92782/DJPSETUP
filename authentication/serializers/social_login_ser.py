from rest_framework import serializers

class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(
        choices=['google', 'github', 'facebook', 'twitter', 'linkedin', 'apple'],
        required=True,
        help_text="Select OAuth provider"
    )
    email = serializers.EmailField(required=True)
