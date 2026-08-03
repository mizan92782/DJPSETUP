from authentication.models.profile_mod import UserProfile
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from authentication.serializers.social_auth_ser import SocialAuthSerializer
from authentication.utils.swg_doc import swagger_documentation
from authentication.utils.auth_utils import create_social_user, generate_tokens
from authentication.services.throtling import SocialAuthThrottle
from authentication.models.user_mod import User
from authentication.models.social_auth_mod import SocialAuth
from shared.responses.responses import custome_success_response, custome_error_response


class SocialAuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet for social authentication (Google, GitHub, Facebook, Twitter, LinkedIn, Apple)
    """
    permission_classes = [AllowAny]
    throttle_classes = [SocialAuthThrottle]
    serializer_class = SocialAuthSerializer
    

    @swagger_documentation(
        title="Social Authentication (Login/Signup)",
        description="Login or register user with Google/GitHub/Facebook/Twitter/LinkedIn/Apple OAuth data. Auto-creates account if new user.",
        request_serializer=SocialAuthSerializer,
        tags=["Social Login"],
        status_code=200,
        method="post"
    )
    @action(detail=False, methods=['post'], url_path='social-login')
    def social_login(self, request):
        """
        Handle social authentication from Google, GitHub, Facebook, Twitter, LinkedIn, or Apple
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        provider = serializer.validated_data['provider']
        provider_id = serializer.validated_data['provider_id']
        
        # Check if social auth exists
        try:
            social_auth = SocialAuth.objects.get(provider=provider, provider_id=provider_id)
            user = social_auth.user
            is_new = False
        except SocialAuth.DoesNotExist:
            # Check if user already exists (email/password registered)
            user = User.objects.filter(email=email).first()
            if user:
                # Link social auth to existing account and log in
                SocialAuth.objects.get_or_create(
                    user=user,
                    provider=provider,
                    defaults={'provider_id': provider_id}
                )
                is_new = False
            else:
                # Create new user and social auth
                try:
                    user, profile, is_new = create_social_user(serializer.validated_data)
                except Exception as e:
                    return custome_error_response(
                        message=f"Failed to create account: {str(e)}",
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                    

        if not user.is_active:
            return custome_error_response(
                message="Account is inactive",
                status_code=status.HTTP_403_FORBIDDEN
            )

        # Always sync profile with latest social auth data
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.first_name = serializer.validated_data.get('first_name', '') or profile.first_name
        profile.last_name = serializer.validated_data.get('last_name', '') or profile.last_name
        profile.dp_image_url = serializer.validated_data.get('dp_image') or profile.dp_image_url
        profile.save(update_fields=['first_name', 'last_name', 'dp_image_url'])

        # Generate tokens
        tokens = generate_tokens(user)

        # Response data
        response_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "is_new": is_new,
                "user_type": "superuser" if user.is_superuser else "staff" if user.is_staff else "user",
            },
            "profile": {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "phone_number": str(profile.phone_number) if profile.phone_number else None,
                "dp_image": profile.dp_image.url if profile.dp_image else profile.dp_image_url,
            },
            "provider": provider,
            "tokens": tokens
        }
        
        message = "Account created successfully" if is_new else "Login successful"
        
        return custome_success_response(
            message=message,
            data_title="user",
            data=response_data,
            status_code=status.HTTP_201_CREATED if is_new else status.HTTP_200_OK
        )
