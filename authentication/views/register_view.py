from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from authentication.serializers.register_ser import RegisterSerializer
from authentication.serializers.otp_request_ser import OTPRequestSerializer
from authentication.serializers.otp_verify_ser import OTPVerifySerializer
from authentication.utils.swg_doc import swagger_documentation
from authentication.utils.auth_utils import (
    generate_otp,
    save_registration_data,
    get_registration_data,
    delete_registration_data,
    send_otp_email,
    verify_otp as verify_otp_hash,
    create_user_with_profile,
    generate_tokens
)
from authentication.services.throtling import SignupUserThrottle, SignupAnonThrottle, OTPThrottle
from shared.responses.responses import custome_success_response, custome_error_response


class RegisterViewSet(viewsets.GenericViewSet):
    """
    ViewSet for user registration with OTP verification
    """
    permission_classes = [AllowAny]
    throttle_classes = [SignupUserThrottle, SignupAnonThrottle, OTPThrottle]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RegisterSerializer
    
    @swagger_documentation(
        title="Request Registration OTP",
        description="Send registration data and receive OTP via email",
        request_serializer=RegisterSerializer,
        tags=["Registration Management"],
        status_code=200,
        method="post"
    )
    @action(detail=False, methods=['post'], url_path='request-otp')
    def request_otp(self, request):
        """Send OTP to email for registration"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        # Generate and send OTP
        otp = generate_otp()
        
        # Prepare data for cache (convert phone_number to string)
        cache_data = serializer.validated_data.copy()
        cache_data['phone_number'] = str(cache_data['phone_number'])
        
        # Save to cache
        save_registration_data(email, otp, cache_data)
        
        # Send OTP email
        try:
            send_otp_email(email, otp)
        except Exception as e:
            return custome_error_response(
                message=f"Failed to send OTP: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return custome_success_response(
            message=f"OTP sent to {email}",
            data_title="email",
            data={"email": email}
        )
    
    @swagger_documentation(
        title="Verify OTP and Register",
        description="Verify OTP and complete user registration",
        request_serializer=OTPVerifySerializer,
        tags=["Registration Management"],
        status_code=201,
        method="post"
    )
    @action(detail=False, methods=['post'], url_path='verify-otp')
    def verify_otp(self, request):
        """Verify OTP and create user account"""
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        # Get cached data
        cached_data = get_registration_data(email)
        if not cached_data:
            return custome_error_response(
                message="OTP expired or not found",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify OTP
        if not verify_otp_hash(otp, cached_data['otp']):
            return custome_error_response(
                message="Invalid OTP",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user and profile
        try:
            user, profile = create_user_with_profile(cached_data)
        except Exception as e:
            return custome_error_response(
                message=f"Failed to create account: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Delete cached data
        delete_registration_data(email)
        

        # Generate tokens
        tokens = generate_tokens(user)

        
        # Response data
        response_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": "user",
            },
            "profile": {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "phone_number": str(profile.phone_number)
            },
            "tokens": tokens
        }
        
        return custome_success_response(
            message="Registration successful",
            data_title="user",
            data=response_data,
            status_code=status.HTTP_201_CREATED
        )
    
    @swagger_documentation(
        title="Resend Registration OTP",
        description="Resend OTP to email when previous OTP expires",
        request_serializer=OTPRequestSerializer,
        tags=["Registration Management"],
        status_code=200,
        method="post"
    )
    @action(detail=False, methods=['post'], url_path='resend-otp')
    def resend_otp(self, request):
        """Resend OTP to email for registration"""
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        # Get cached data
        cached_data = get_registration_data(email)
        if not cached_data:
            return custome_error_response(
                message="No registration found for this email. Please start registration again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate new OTP
        otp = generate_otp()
        
        # Update cache with new OTP
        save_registration_data(email, otp, cached_data)
        
        # Send OTP email
        try:
            send_otp_email(email, otp)
        except Exception as e:
            return custome_error_response(
                message=f"Failed to send OTP: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return custome_success_response(
            message=f"OTP resent to {email}",
            data_title="email",
            data={"email": email}
        )
