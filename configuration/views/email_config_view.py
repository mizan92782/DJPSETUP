"""
configuration/views/email_config_view.py — Email Configuration ViewSet
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from shared.permissions.permissions import IsAdmin
from shared.responses.responses import custome_success_response, custome_error_response
from configuration.models.email_config_mod import EmailConfiguration
from configuration.serializers.email_config_ser import EmailConfigurationSerializer


class EmailConfigurationViewSet(viewsets.GenericViewSet):
    """Admin-only ViewSet to read and update email configuration."""
    serializer_class = EmailConfigurationSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return EmailConfiguration.objects.first()

    def list(self, request):
        instance = self.get_object()
        if not instance:
            return custome_error_response(
                message="No email configuration found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return custome_success_response(
            message="Email configuration retrieved successfully.",
            data_title="email_configuration",
            data=serializer.data,
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return custome_error_response(
                message="No email configuration found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custome_success_response(
            message="Email configuration updated successfully.",
            data_title="email_configuration",
            data=serializer.data,
        )
