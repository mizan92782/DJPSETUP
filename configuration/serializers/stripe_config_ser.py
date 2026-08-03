"""
configuration/serializers/stripe_config_ser.py
"""
from rest_framework import serializers
from configuration.models.stripe_config_mod import StripeConfiguration


class StripeConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeConfiguration
        fields = ['stripe_secret_key', 'stripe_publishable_key', 'stripe_webhook_secret']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StripePublicKeySerializer(serializers.ModelSerializer):
    """Read-only serializer exposing only the publishable key for client use."""
    class Meta:
        model = StripeConfiguration
        fields = ['stripe_publishable_key']
        read_only_fields = ['stripe_publishable_key']
