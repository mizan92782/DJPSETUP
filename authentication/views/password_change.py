from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from authentication.serializers.pass_change import ChangeProfilePasswordSerializer
from shared.responses.responses import custome_success_response, custome_error_response


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangeProfilePasswordSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch', 'head', 'options']

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary="Change Password",
        operation_description="Change password for authenticated user",
        request_body=ChangeProfilePasswordSerializer,
        tags=["Password Management"],
        responses={200: "Password changed successfully"}
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        

        return custome_success_response(
            message="Password changed successfully",
            data_title="success",
            data={"detail": "Password changed successfully"}
        )
        
