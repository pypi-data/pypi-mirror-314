import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.state import token_backend
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class CustomUser:
    def __init__(self, user_id):
        self.id = user_id
        self.username = f"user_{user_id}"
        self.is_authenticated = True

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that extends JWTAuthentication.
    This class handles the authentication process using JWT tokens.
    """

    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        """
        Authenticates the request using JWT token.
        Args:
            request (HttpRequest): The request object.
            url (str): The URL to send the token for validation.
        Returns:
            tuple: A tuple containing the authenticated user and the raw token.
        Raises:
            AuthenticationFailed: If the authorization credentials were not provided or the token is invalid.
        """
        # TODO: CustomJWTAuthentication is passed to View classes via
        # authentication_classes, is it possible to pass it so it can be used in
        # __init__?
        # complication arises because CustomJWTAuthentication is passed as a
        # class and not an object(i.e., instance of class)
        if self.url is None:
            self.url = 'http://127.0.0.1:8001/jwt/token/verify/' # take out to env file

        header = self.get_header(request)
        if header is None:
            logger.error("Header not provided ")
            raise AuthenticationFailed("Header not provided")

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            logger.error("Authorization credentials were not provided")
            raise AuthenticationFailed("Authorization credentials were not provided")

        try:
            validated_token = token_backend.decode(raw_token, verify=True)
            user_id = validated_token.get('emp_num', None)
            print(f"\n\n====================================================\n\nUser ID: {user_id}\n\n====================================================\n\n")
        except Exception as e:
            logger.error(f"Invalid token: {e}")
            print(f"Invalid token: {e}")
            raise InvalidToken(e) from e

        if not validated_token or user_id is None:
            logger.error("Invalid token or No user ID found.")
            raise InvalidToken("Invalid token or No user ID found.")

        AppUser = get_user_model()
         # Ensure AppUser is compared correctly
        expected_model = 'auth_n_auth.models.AppUsers'  # Use the full path of the model

        if AppUser.__module__ + '.' + AppUser.__qualname__ != expected_model:
            app_user = CustomUser(user_id)
            request.user = app_user  # Set to user instance, not just ID
            return app_user, raw_token
        else:
            try:
                app_user = AppUser.objects.get(emp_num=user_id)
                request.user = app_user  # Set to user instance, not just ID
                try:
                    authenticated = super().authenticate(request)
                    return authenticated
                except Exception as e:
                    print(f"Error authenticating: {e}")
                    raise AuthenticationFailed("Error authenticating") from e
            except AppUser.DoesNotExist:
                print(f"\nUser with ID {user_id} does not exist")
                logger.error(f"User with ID {user_id} does not exist")
                raise AuthenticationFailed("Invalid user")
            except Exception as e:
                print(f"\nError fetching user: {e}")
                logger.error(f"Error fetching user: {e}")
                raise AuthenticationFailed("Error fetching user") from e
