from authentication.models.user_mod import User

def UserCreation(data):
    try:
        return User.objects.create_user(
            email=data.pop("email"),
            password=data.pop("password"),
        )
    except Exception as e:
        raise Exception(f"User creation failed: {str(e)}") from e
