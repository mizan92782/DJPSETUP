from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import EmailConfiguration, CertificateTemplate
from .serializers import EmailConfigurationSerializer, CertificateTemplateSerializer, CertificateTemplatePublicSerializer
from shared.permissions.permissions import IsAdmin
from shared.responses.responses import custome_success_response, custome_error_response


class EmailConfigurationViewSet(viewsets.GenericViewSet):
    queryset = EmailConfiguration.objects.all()
    serializer_class = EmailConfigurationSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return EmailConfiguration.objects.first()

    @swagger_auto_schema(
        tags=['Settings - Email Settings'],
        operation_summary='Get Email Configuration',
        operation_description=(
            '## Retrieve the singleton email configuration.\n\n'
            '> **Permission:** Super admin only (`is_superuser=True`)\n\n'
            'Returns the single email configuration object.'
        ),
        responses={
            200: EmailConfigurationSerializer,
            401: 'Unauthorized',
            403: 'Forbidden - Super admin access required',
        }
    )
    def list(self, request, *args, **kwargs):
        config = self.get_object()
        serializer = self.get_serializer(config)
        return custome_success_response(
            data=serializer.data,
            message="Email configuration retrieved"
        )

    def update(self, request, *args, **kwargs):
        config = self.get_object()
        serializer = self.get_serializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custome_success_response(
            data=serializer.data,
            message="Email configuration updated successfully"
        )

    @swagger_auto_schema(
        tags=['Settings - Email Settings'],
        operation_summary='Update Email Configuration',
        operation_description=(
            '## Update the singleton email configuration.\n\n'
            '> **Permission:** Super admin only\n\n'
            'All fields are optional.'
        ),
        request_body=EmailConfigurationSerializer,
        responses={
            200: EmailConfigurationSerializer,
            400: 'Validation error',
            401: 'Unauthorized',
            403: 'Forbidden - Super admin access required',
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


class CertificateTemplateViewSet(viewsets.GenericViewSet):
    serializer_class = CertificateTemplateSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        obj, _ = CertificateTemplate.objects.get_or_create(pk=1)
        return obj

    @swagger_auto_schema(
        tags=['Admin - Certificate Template'],
        operation_summary='Get Certificate Template',
        operation_description=(
            '## Retrieve the singleton certificate template.\n\n'
            '> **Permission:** Super admin only (`is_superuser=True`)'
        ),
        responses={
            200: CertificateTemplateSerializer,
            401: 'Unauthorized',
            403: 'Forbidden - Super admin access required',
        }
    )
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return custome_success_response(
            data=serializer.data,
            message="Certificate template retrieved"
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custome_success_response(
            data=serializer.data,
            message="Certificate template updated successfully"
        )

    @swagger_auto_schema(
        tags=['Admin - Certificate Template'],
        operation_summary='Update Certificate Template',
        operation_description=(
            '## Update the singleton certificate template.\n\n'
            '> **Permission:** Super admin only\n\n'
            'Send files as multipart/form-data. All fields are optional.'
        ),
        manual_parameters=[
            openapi.Parameter('platform_icon', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('university_logo', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('signature', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('seal', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('collaborator_logo', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('certificate_template', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('university_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('professor_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('endorser_first_designation', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('endorser_second_designation', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        ],
        consumes=['multipart/form-data'],
        responses={
            200: CertificateTemplateSerializer,
            400: 'Validation error',
            401: 'Unauthorized',
            403: 'Forbidden - Super admin access required',
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CertificateTemplatePublicView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['certificate_template'],
        operation_summary='Get Certificate Template (Public)',
        operation_description='Returns the certificate template data. No authentication required.',
        responses={200: CertificateTemplateSerializer},
    )
    def get(self, request):
        obj, _ = CertificateTemplate.objects.get_or_create(pk=1)
        serializer = CertificateTemplatePublicSerializer(obj, context={'request': request})
        return custome_success_response(
            data=serializer.data,
            message="Certificate template retrieved"
        )
