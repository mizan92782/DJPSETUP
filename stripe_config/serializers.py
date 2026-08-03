from rest_framework import serializers

from .models import StripeConfiguration


class StripeConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeConfiguration
        fields = [
            'stripe_secret_key',
            'stripe_publishable_key',
            'stripe_webhook_secret',
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StripePublicKeySerializer(serializers.ModelSerializer):
    """
    Serializer for public access to Stripe publishable key only.
    """

    class Meta:
        model = StripeConfiguration
        fields = ['stripe_publishable_key']
        read_only_fields = ['stripe_publishable_key']
