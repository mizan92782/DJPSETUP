from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from authentication.models.profile_mod import UserProfile
from authentication.models.admin_profile_mod import AdminProfile
from authentication.serializers.profile_ser import UserProfileSerializer, AdminProfileSerializer
from authentication.utils.swg_doc import swagger_documentation
from shared.responses.responses import custome_success_response, custome_error_response


class ProfileViewSet(viewsets.GenericViewSet):
    """
    ViewSet for current user's profile management
    No ID required - automatically uses logged-in user
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on user type"""
        if self.request.user.is_superuser or self.request.user.is_staff:
            return AdminProfileSerializer
        return UserProfileSerializer
    
    def get_object(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            profile, _ = AdminProfile.objects.get_or_create(
                user=user,
                defaults={'first_name': user.email.split('@')[0], 'last_name': ''},
            )
            return profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    @action(detail=False, methods=['get'], url_path='me')
    @swagger_documentation(
        title="Get My Profile",
        description="Get current logged-in user's profile. Returns UserProfile for regular users, AdminProfile for staff/superusers.",
        response_serializer=UserProfileSerializer,
        tags=["Profile Management"],
        status_code=200
    )
    def me(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custome_success_response(
            message="Profile retrieved successfully",
            data_title="profile",
            data=serializer.data
        )

    @action(detail=False, methods=['patch'], url_path='update')
    @swagger_documentation(
        title="Update My Profile",
        description="Partial update of current user's profile. Regular users: first_name, last_name, phone_number, dp_image. Admin users: same + department.",
        request_serializer=UserProfileSerializer,
        response_serializer=UserProfileSerializer,
        tags=["Profile Management"],
        status_code=200
    )
    def update_profile(self, request):
        instance = self.get_object()
        if request.data.get('remove_image') in ['true', 'True', '1', True]:
            instance.dp_image.delete(save=True)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custome_success_response(
            message="Profile updated successfully",
            data_title="profile",
            data=serializer.data
        )
    
    @action(detail=False, methods=['patch'], url_path='remove-image')
    def remove_image(self, request):
        instance = self.get_object()
        instance.dp_image.delete(save=True)
        return custome_success_response(
            message="Profile image removed successfully",
            data_title="profile",
            data=self.get_serializer(instance).data
        )

    @action(detail=False, methods=['delete'], url_path='delete')
    @swagger_documentation(
        title="Delete User Account and Profile",
        description="Permanently delete current user account and associated profile data",
        tags=["Profile Management"],
        status_code=204
    )
    def delete_account(self, request):
        """Delete current user account and profile"""
        user = request.user
        
        try:
            # Delete user (cascade will delete profile)
            user.delete()
            
            return custome_success_response(
                message="Account and profile deleted successfully",
                data_title="deleted",
                data={"deleted": True},
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return custome_error_response(
                message=f"Failed to delete account: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
