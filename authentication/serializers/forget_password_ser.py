from rest_framework import serializers

class PasswordForgetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class ResetPasswordSerializer(serializers.Serializer):
    reset_token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)