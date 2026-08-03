import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_yasg.utils import swagger_auto_schema


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(
        operation_summary="Logout",
        operation_description="Blacklist refresh token and log out the authenticated user. Send refresh token in request body.",
        tags=["Registration Management"],
        responses={
            205: "Logout successful",
            400: "Invalid or missing token",
            401: "Unauthorized",
        }
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError:
            return Response(
                {
                    "error": "Invalid or expired token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
