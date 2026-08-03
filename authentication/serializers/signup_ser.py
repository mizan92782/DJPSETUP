import phonenumber_field.modelfields
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField 


class RegisterRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    phone_number = PhoneNumberField()
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        
        if len(attrs["password"]) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters"}  )
        
            
        return attrs

        
        
        
        

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
