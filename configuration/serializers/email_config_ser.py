"""
configuration/serializers/email_config_ser.py
"""
from rest_framework import serializers
from configuration.models.email_config_mod import EmailConfiguration


class EmailConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfiguration
        fields = ['email_host', 'email_address', 'email_password', 'port', 'use_tls']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
