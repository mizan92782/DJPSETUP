from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Refresh Access Token",
        operation_description="Refresh expired access token using refresh token. Send refresh token in request body.",
        tags=["Registration Management"],
        responses={
            200: openapi.Response(description="New access token generated"),
            400: "Invalid or expired refresh token",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
