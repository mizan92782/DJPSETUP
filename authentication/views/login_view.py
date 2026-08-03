from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone

from authentication.serializers.login_ser import LoginSerializer
from authentication.utils.swg_doc import swagger_documentation
from authentication.utils.auth_utils import authenticate_user, generate_tokens
from authentication.services.throtling import LoginUserThrottle, LoginAnonThrottle
from shared.responses.responses import custome_success_response, custome_error_response


class LoginViewSet(viewsets.GenericViewSet):
    """
    ViewSet for user login
    """
    permission_classes = [AllowAny]
    throttle_classes = [LoginUserThrottle, LoginAnonThrottle]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = LoginSerializer
    
    @swagger_documentation(
        title="User Login",
        description="Login with email and password to get JWT tokens",
        request_serializer=LoginSerializer,
        tags=["Registration Management"],
        status_code=200,
        method="post"
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Authenticate user and return tokens"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate_user(email, password)
        
        if not user:
            return custome_error_response(
                message="Invalid email or password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return custome_error_response(
                message="Account is inactive",
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        # Generate tokens
        tokens = generate_tokens(user)

        # Update last_login — JWT bypasses Django's session login so we set it manually
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        # Get profile data
        profile_data = None
        if user.is_superuser or user.is_staff:
            if hasattr(user, 'admin_profile'):
                p = user.admin_profile
                profile_data = {
                    'first_name': p.first_name,
                    'last_name': p.last_name,
                    'phone_number': p.phone_number,
                    'department': p.department,
                }
        elif hasattr(user, 'profile'):
            p = user.profile
            profile_data = {
                'first_name': p.first_name,
                'last_name': p.last_name,
                'phone_number': str(p.phone_number) if p.phone_number else None,
            }
        
        response_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": "superuser" if user.is_superuser else "staff" if user.is_staff else "user",
            },
            "profile": profile_data,
            "tokens": tokens
        }
        
        return custome_success_response(
            message="Login successful",
            data_title="user",
            data=response_data
        )
