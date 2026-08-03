from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.views.register_view import RegisterViewSet
from authentication.views.login_view import LoginViewSet
from authentication.views.profile_new_view import ProfileViewSet
from authentication.views.social_auth_view import SocialAuthViewSet
from authentication.views.forget_pass_view import PasswordForgetRequestView, PasswordForgetVerifyOTPView, ResetPasswordView, ResendPasswordResetOTPView
from authentication.views.logout_view import LogoutView
from authentication.views.password_change import ChangePasswordView
from authentication.views.token_refresh_view import CustomTokenRefreshView

router = DefaultRouter()
router.register(r'signup', RegisterViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'social', SocialAuthViewSet, basename='social')

urlpatterns = [
  
    path('', include(router.urls)),
    
    # Auth
    path('refresh_token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Password Reset
    path('password_forget/request-otp/', PasswordForgetRequestView.as_view()),
    path('password_forget/verify-otp/', PasswordForgetVerifyOTPView.as_view()),
    path('password_forget/resend-otp/', ResendPasswordResetOTPView.as_view()),
    path('password_reset/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
