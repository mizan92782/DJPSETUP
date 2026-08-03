import traceback
from authentication.models.profile_mod import UserProfile

def ProfileCreation(data, created_user):
    try:
        # Remove unwanted fields
        data.pop("email", None)
        data.pop("password", None)
        data.pop("password2", None)
        data.pop("otp", None)
        # Create profile
        profile = UserProfile.objects.create(
            user=created_user,
            **data
        )


        return profile

    except Exception as e:
        print("Profile Creation Error:")
        traceback.print_exc()
        raise Exception(f"Profile not created: {str(e)}") from e
