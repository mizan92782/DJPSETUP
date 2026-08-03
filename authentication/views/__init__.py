"""
Authentication Views Package
"""
from authentication.views.register_view import RegisterViewSet
from authentication.views.login_view import LoginViewSet
from authentication.views.logout_view import LogoutView
from authentication.views.profile_new_view import ProfileViewSet
from authentication.views.social_auth_view import SocialAuthViewSet
from authentication.views.forget_pass_view import (
    PasswordForgetRequestView,
    PasswordForgetVerifyOTPView,
    ResetPasswordView,
    ResendPasswordResetOTPView,
)
from authentication.views.password_change import ChangePasswordView
from authentication.views.token_refresh_view import CustomTokenRefreshView

__all__ = [
    "RegisterViewSet",
    "LoginViewSet",
    "LogoutView",
    "ProfileViewSet",
    "SocialAuthViewSet",
    "PasswordForgetRequestView",
    "PasswordForgetVerifyOTPView",
    "ResetPasswordView",
    "ResendPasswordResetOTPView",
    "ChangePasswordView",
    "CustomTokenRefreshView",
]
