from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.services.throtling import OTPThrottle, PasswordResetThrottle
from django.core.cache import cache
import json
import uuid
from authentication.models.user_mod import User
from authentication.services.otp import GENERATE_OTP, MATCH_HASED_OTP
from authentication.utils.send_email import SEND_OTP_EMAIL
from authentication.serializers.forget_password_ser import PasswordForgetRequestSerializer, ResetPasswordSerializer
from authentication.serializers.signup_ser import OTPVerifySerializer
from authentication.utils.constants import APP_NAME
from shared.responses.responses import custome_success_response, custome_error_response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class PasswordForgetRequestView(generics.GenericAPIView):
    serializer_class = PasswordForgetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Request Password Reset OTP",
        operation_description="Send password reset OTP to user email. Send email in request body.",
        tags=["Password Management"],
        responses={
            200: openapi.Response(description="OTP sent"),
            404: "User not found",
            400: "Validation error",
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if not User.objects.filter(email=email).exists():
            return custome_error_response(
                message="No account found with this email address. Please check and try again.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        otp = GENERATE_OTP()
        
        from authentication.services.otp import HASH_OTP
        from django.conf import settings
        data = {"otp": HASH_OTP(otp)}
        cache.set(
            key=f"password_forget:{email}",
            value=json.dumps(data),
            timeout=settings.OTP_EXPIRE_TIME,
        )

        try:
            SEND_OTP_EMAIL(f"Password Reset OTP - {APP_NAME}", email, otp)
        except Exception:
            pass

        return custome_success_response(
            message=f"A password reset OTP has been sent to {email}. Please check your inbox and enter the code to proceed.",
            status_code=status.HTTP_200_OK
        )


class ResendPasswordResetOTPView(generics.GenericAPIView):
    serializer_class = PasswordForgetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Resend Password Reset OTP",
        operation_description="Resend a fresh OTP to the user's email. Old OTP is invalidated.",
        tags=["Password Management"],
        responses={
            200: openapi.Response(description="OTP resent"),
            404: "User not found",
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if not User.objects.filter(email=email).exists():
            return custome_error_response(
                message="No account found with this email address.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # পুরনো OTP delete করো
        cache.delete(f"password_forget:{email}")

        # নতুন OTP তৈরি করো
        otp = GENERATE_OTP()

        from authentication.services.otp import HASH_OTP
        from django.conf import settings
        data = {"otp": HASH_OTP(otp)}
        cache.set(
            key=f"password_forget:{email}",
            value=json.dumps(data),
            timeout=settings.OTP_EXPIRE_TIME,
        )

        try:
            SEND_OTP_EMAIL(f"Password Reset OTP - {APP_NAME}", email, otp)
        except Exception:
            pass

        return custome_success_response(
            message=f"A new OTP has been sent to {email}. The previous OTP is no longer valid.",
            status_code=status.HTTP_200_OK
        )

        
class PasswordForgetVerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]
    parser_classes = [MultiPartParser, FormParser]
    
    @swagger_auto_schema(
        operation_summary="Verify Password Reset OTP",
        operation_description="Verify OTP and return reset token. Send email and otp in request body.",
        tags=["Password Management"],
        responses={
            200: openapi.Response(description="OTP verified"),
            400: "Invalid OTP / OTP expired",
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        cached_data = cache.get(f"password_forget:{email}")
        if not cached_data:
            return custome_error_response(
                message="The OTP has expired. Please request a new one to continue.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = json.loads(cached_data)
        if not MATCH_HASED_OTP(otp, data["otp"]):
            return custome_error_response(
                message="The OTP you entered is incorrect. Please verify and try again.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        reset_token = str(uuid.uuid4())
        cache.set(
            f"password_reset_token:{reset_token}",
            email,
            timeout=300,
        )
        cache.delete(f"password_forget:{email}")

        return custome_success_response(
            data_title="reset_token",
            data=reset_token,
            message="OTP verified successfully. You can now reset your password.",
            status_code=status.HTTP_200_OK
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetThrottle]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Reset Password",
        operation_description="Reset password with a valid reset token. Send reset_token and new_password in request body.",
        tags=["Password Management"],
        responses={
            200: openapi.Response(description="Password reset successful"),
            400: "Invalid token / validation error",
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        email = cache.get(f"password_reset_token:{reset_token}")
        if not email:
            return custome_error_response(
                message="Invalid or expired reset token. Please request a new password reset.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        cache.delete(f"password_reset_token:{reset_token}")

        return custome_success_response(
            message="Your password has been reset successfully. You can now log in with your new password.",
            status_code=status.HTTP_200_OK
        )

        
