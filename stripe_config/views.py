from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import StripeConfiguration
from .serializers import StripeConfigurationSerializer, StripePublicKeySerializer
from shared.permissions.permissions import IsAdmin
from shared.responses.responses import custome_success_response, custome_error_response


class StripeConfigurationViewSet(viewsets.GenericViewSet):
    """
    API endpoint for managing the singleton Stripe configuration.
    Only one configuration object exists in the system.
    Only admin users (superusers) can access these endpoints.
    """
    queryset = StripeConfiguration.objects.all()
    serializer_class = StripeConfigurationSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        """Always return the singleton stripe configuration."""
        return StripeConfiguration.objects.first()
    @swagger_auto_schema(
        tags=['Settings - Stripe Settings'],
        operation_summary='Get Stripe Configuration',
        operation_description=(
            '## Retrieve the singleton Stripe configuration.\n\n'
            '> **Permission:** Super admin only (`is_superuser=True`)\n\n'
            'Returns the single Stripe configuration object. '
            'If none exists, one is created with default empty values.'
        ),
        responses={
            200: StripeConfigurationSerializer,
            401: 'Unauthorized',
            403: 'Forbidden - Super admin access required',
        }
    )
    def list(self, request, *args, **kwargs):
        config = self.get_object()
        serializer = self.get_serializer(config)
        return custome_success_response(
            data=serializer.data,
            message="Stripe configuration retrieved"
        )

    def update(self, request, *args, **kwargs):
        config = self.get_object()
        serializer = self.get_serializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custome_success_response(
            data=serializer.data,
            message="Stripe configuration updated successfully"
        )

    @swagger_auto_schema(
        tags=['Settings - Stripe Settings'],
        operation_summary='Update Stripe Configuration',
        operation_description=(
            '## Update the singleton Stripe configuration.\n\n'
            '> **Permission:** Super admin only\n\n'
            '**Request body:** (all fields optional)\n'
            '```json\n'
            '{\n'
            '  "stripe_secret_key": "sk_live_123",\n'
            '  "stripe_publishable_key": "pk_live_123",\n'
            '  "stripe_webhook_secret": "whsec_123"\n'
            '}\n'
            '```\n\n'
            '**Notes:**\n'
            '- Only one configuration exists; this updates it.\n'
            '- Keys are only updated if explicitly provided.'
        ),
        request_body=StripeConfigurationSerializer,
        responses={
            200: openapi.Response(
                description='Configuration updated successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Stripe configuration updated successfully',
                        'data': {
                            'stripe_secret_key': 'sk_test_123',
                            'stripe_publishable_key': 'pk_test_123'
                        }
                    }
                }
            ),
            400: 'Validation error',
            401: 'Unauthorized',
            403: 'Forbidden - Super admin access required',
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        
        serializer.save()


class StripePublicKeyView(APIView):
    """
    Public API endpoint to retrieve only the Stripe publishable key.
    No authentication required - accessible to all users.
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=['Settings - Stripe Settings'],
        operation_summary='Get Stripe Publishable Key (Public)',
        operation_description=(
            '## Retrieve the Stripe publishable key for client-side use.\n\n'
            '> **Permission:** Public - No authentication required\n\n'
            'Returns only the publishable key (pk_test_xxx or pk_live_xxx) '
            'which is safe to expose on the client side. '
            'The secret key is never exposed through this endpoint.'
        ),
        responses={
            200: openapi.Response(
                description='Publishable key retrieved successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Stripe publishable key retrieved',
                        'data': {
                            'stripe_publishable_key': 'pk_test_51ABC123...'
                        }
                    }
                }
            ),
            404: 'Stripe configuration not found',
        }
    )
    def get(self, request, *args, **kwargs):
        """Get the Stripe publishable key."""
        config = StripeConfiguration.objects.first()
        
        if not config:
            return custome_success_response(
                data={'stripe_publishable_key': ''},
                message="Stripe configuration not found",
                status_code=404
            )
        
        serializer = StripePublicKeySerializer(config)
        return custome_success_response(
            data=serializer.data,
            message="Stripe publishable key retrieved"
        )
