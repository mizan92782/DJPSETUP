"""
configuration/views/stripe_config_view.py — Stripe Configuration ViewSet
Merged from stripe_config app.
"""
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from shared.permissions.permissions import IsAdmin
from shared.responses.responses import custome_success_response, custome_error_response
from configuration.models.stripe_config_mod import StripeConfiguration
from configuration.serializers.stripe_config_ser import StripeConfigurationSerializer, StripePublicKeySerializer


class StripeConfigurationViewSet(viewsets.GenericViewSet):
    """Admin-only ViewSet to read and update Stripe configuration."""
    serializer_class = StripeConfigurationSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return StripeConfiguration.objects.first()

    def list(self, request):
        instance = self.get_object()
        if not instance:
            return custome_error_response(
                message="No Stripe configuration found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return custome_success_response(
            message="Stripe configuration retrieved successfully.",
            data_title="stripe_configuration",
            data=serializer.data,
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return custome_error_response(
                message="No Stripe configuration found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Re-apply Stripe config to Django settings at runtime
        try:
            from configuration.services.stripe_config import apply_stripe_config
            apply_stripe_config()
        except Exception:
            pass

        return custome_success_response(
            message="Stripe configuration updated successfully.",
            data_title="stripe_configuration",
            data=serializer.data,
        )


class StripePublicKeyView(APIView):
    """Public endpoint — returns only the Stripe publishable key."""
    permission_classes = [AllowAny]

    def get(self, request):
        config = StripeConfiguration.objects.first()
        if not config:
            return custome_error_response(
                message="Stripe configuration not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = StripePublicKeySerializer(config)
        return custome_success_response(
            message="Stripe public key retrieved successfully.",
            data_title="stripe",
            data=serializer.data,
        )
