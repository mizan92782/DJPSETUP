# from rest_framework import mixins, viewsets, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.parsers import MultiPartParser, FormParser

# from authentication.model.profile_mod import CustomerProfile
# from authentication.model.user_mod import User
# from authentication.services.customer_profile import createCustomerProfile
# from pro_utilities.permissions import IsCustomer
# from pro_utilities.swagger_doc import swagger_documentation


# class CustomerProfileViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet
# ):
    
    
#     serializer_class = CustomerProfileSerializer
#     permission_classes = [IsCustomer]          #!-------for show form data in swagger-------------->>
#     parser_classes = [MultiPartParser, FormParser]
#     http_method_names = ['get', 'post', 'patch', 'delete']

#     def get_queryset(self):
#         # drf-yasg schema generation time
#         if getattr(self, "swagger_fake_view", False):
#             return CustomerProfile.objects.none()
            
#         user = self.request.user
#         if not user or not user.is_authenticated:
#             return CustomerProfile.objects.none()

#         return CustomerProfile.objects.filter(user=user)

   
    
    
    
    
    
    
        
        
        
        
        
        
#     # ---------------- PARTIAL UPDATE ----------------
#     @swagger_documentation(
#         title="Update customer profile",
#         description="Partially update customer profile",
#         serializer=CustomerProfileSerializer,
#         tags=["Customer Profile"],
#     )
#     @action(detail=False, methods=['patch'], url_path='update-me')
#     def update_me(self, request):
#         instance = CustomerProfile.objects.filter(user=request.user).first()
        
#         if not instance:
#             return Response(
#                 {"message": "No profile found for current user"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "message": "Customer Profile updated successfully",
#                 "customer": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

        
        
        
        
        
        
        
        
#     # ---------------- DELETE ----------------
#     @swagger_documentation(
#         title="Delete customer profile",
#         description="Delete authenticated user's profile and account",
#         tags=["Customer Profile"],
#         status_code=204,
#         method="delete" # Use delete method to avoid request body in swagger
#     )
#     @action(detail=False, methods=['delete'], url_path='delete-me')
#     def delete_me(self, request):
#         user = request.user
#         user.delete()
#         return Response(
#             {"message": "User account and profile deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )

        
        
        
        
        
        
        
        
#     # ---------------- ME (CUSTOM ACTION) ----------------
#     @swagger_documentation(
#         title="Get current user profile",
#         description="Fetch profile of logged-in user",
#         serializer=CustomerProfileSerializer,
#         method="get",   
#         tags=["Customer Profile"],
#     )
#     @action(detail=False, methods=['get'], url_path='me')
#     def me(self, request):
#         instance = CustomerProfile.objects.filter(user=request.user).first()

#         if not instance:
#             return Response(
#                 {"message": "No profile found for current user"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = self.get_serializer(instance)
#         return Response(
#             {
#                 "message": "Current user profile fetched successfully",
#                 "customer": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )
        