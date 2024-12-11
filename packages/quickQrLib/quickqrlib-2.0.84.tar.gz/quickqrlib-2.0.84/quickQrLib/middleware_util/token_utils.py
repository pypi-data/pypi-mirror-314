from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import requests
import base64
import json
import time
import jwt
from jwt.exceptions import DecodeError
from rest_framework_simplejwt.settings import api_settings
from requests.exceptions import RequestException

class TokenUtils:
    @classmethod
    def get_tokens_for_user_inline(cls, user):
        token = RefreshToken.for_user(user)
        return str(token), str(token.access_token)

    @classmethod
    def get_tokens_for_user(cls, user, base_url: str = 'http://127.0.0.1:8001/'):
        token_obtain_url = base_url + 'token/'
        data = {
            'email': user.email,
            'user_id': user.id,
            'emp_id': user.emp_id
        }
        try:
            response = requests.post(token_obtain_url, data=data)
            response_data = response.json()
            access_token = response_data.get('access', None)
            refresh_token = response_data.get('refresh', None)

            if access_token and refresh_token:
                print (f"No access token: {access_token} and refresh token: {refresh_token}")
                return access_token, refresh_token
            else:
                return None, None
        except Exception as e:
            print(f'Token Obtain Error: {e}')
            return None, None

    @classmethod
    def refresh_access_token(cls, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return new_access_token
        except Exception as e:
            print(f'Token Refresh Error: {e}')
            return None

    @classmethod
    def verify_token(cls, access_token):
        try:
            token = AccessToken(access_token)
            success, info = token.verify()
            return success, info
        except Exception as e:
            print(f'Token Verify Error: {e}')
            return False, str(e)

    @classmethod
    def decode_token(cls, token):
        try:
            # Decode token to inspect the payload without verifying the signature
            verifying_key = api_settings.VERIFYING_KEY
            decoded_token = jwt.decode(token, verifying_key, algorithms=['RS256'], options={"verify_signature": True})
            return decoded_token
        except jwt.InvalidSignatureError as e:
            print(f"Invalid Signature Error: {e}")
            return None
        except DecodeError as e:
            print(f"Invalid token: {e}")
            return None
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None

    @classmethod
    def get_expiry(cls, jwt_token):
        import datetime
        if type(jwt_token) == dict:
            payload = jwt_token.get('exp', None)
            return payload
        else:
            payload = jwt_token.split('.')[1]
            # Add padding to fix incorrect token length
            payload += '=' * (-len(payload) % 4)
            decoded_payload = base64.b64decode(payload)
            payload_json = json.loads(decoded_payload)
            #Convert exp to datetime
            expiry = payload_json['exp']
            # Convert Unix timestamp to datetime object
            expiry_datetime = datetime.datetime.fromtimestamp(expiry)
            return payload_json['exp']

    @classmethod
    def is_token_expired(cls, jwt_token):
        expiry = cls.get_expiry(jwt_token)
        check_time = time.time()
        return check_time > expiry

    @classmethod
    def validate_token(cls, token):
        try:
            # Validate token by creating an UntypedToken instance
            decoded_token = cls.decode_token(token)
            generic_token = UntypedToken(token, verify=True)
            verify = generic_token.verify()
            if not decoded_token:
                raise jwt.InvalidSignatureError
            if verify:
                raise InvalidToken(verify)
            if cls.is_token_expired(decoded_token):
                raise TokenError('Token expired')
            return True
        except InvalidToken as e:
            print(f"Token validation error: {e}")
            return False
        except TokenError as e:
            print(f"Token error in Validate Token: {e}")
            return False
        except jwt.InvalidSignatureError as e:
            print(f"Invalid Signature Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during token validation: {e}")
            return False

    @classmethod
    def check_blacklist(cls, token, token_type="refresh"):
        blacklist = cls.get_blacklist()
        if not blacklist.get('refresh_tokens', None) and not blacklist.get('access_tokens', None):
            print ("\n\nNo tokens in blacklist\n\n")
            return True
        refresh_tokens = blacklist.get('refresh_tokens', None)
        access_tokens = blacklist.get('access_tokens', None)
        if token_type == "refresh":
            for r_token in refresh_tokens:
                if r_token == token:
                    return False
        if token_type == "access":
            if isinstance(token, list):
                token = token[0]
            elif isinstance(token, str):
                token = token.split(' ')
                if len(token) > 1:
                    token = token[1]
            for a_token in access_tokens:
                if a_token == token:
                    return False
        return True

    @classmethod
    def get_blacklist(cls, base_url: str = 'http://127.0.0.1:8001/'):
        url = base_url + 'jwt/blacklist/all/'
        try:
            response = requests.get(url)
            response_data = response.json()
            return response_data
        except RequestException as e:
            print(f"Error getting blacklist: {e}")
            return None
