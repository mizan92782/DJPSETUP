"""
configuration/views/certificate_view.py — Certificate Template ViewSet
"""
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from shared.permissions.permissions import IsAdmin
from shared.responses.responses import custome_success_response, custome_error_response
from configuration.models.certificate_mod import CertificateTemplate
from configuration.serializers.certificate_ser import CertificateTemplateSerializer, CertificateTemplatePublicSerializer


class CertificateTemplateViewSet(viewsets.GenericViewSet):
    """Admin-only ViewSet to read and update certificate template."""
    serializer_class = CertificateTemplateSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return CertificateTemplate.objects.first()

    def list(self, request):
        instance = self.get_object()
        if not instance:
            return custome_error_response(
                message="No certificate template found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return custome_success_response(
            message="Certificate template retrieved successfully.",
            data_title="certificate_template",
            data=serializer.data,
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return custome_error_response(
                message="No certificate template found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custome_success_response(
            message="Certificate template updated successfully.",
            data_title="certificate_template",
            data=serializer.data,
        )


class CertificateTemplatePublicView(APIView):
    """Public endpoint — returns only the certificate template file."""
    permission_classes = [AllowAny]

    def get(self, request):
        instance = CertificateTemplate.objects.first()
        if not instance:
            return custome_error_response(
                message="No certificate template found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = CertificateTemplatePublicSerializer(instance)
        return custome_success_response(
            message="Certificate template retrieved.",
            data_title="certificate_template",
            data=serializer.data,
        )
