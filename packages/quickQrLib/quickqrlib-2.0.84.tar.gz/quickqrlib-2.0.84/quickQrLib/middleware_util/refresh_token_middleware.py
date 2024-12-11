from fnmatch import fnmatch
from django.http import HttpResponse
from quickQrLib.middleware_util.token_utils import TokenUtils

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0
        self.token_generator = TokenUtils()
        self.ignore_paths = [
            '/token/refresh/', '/token/', '/token/verify/', '/login/', '/metrics', '/metrics/', '/admin/',
            '/admin/login/', '/forgot-password/', '/health/', '/verify-client/',
            '/jwt/blacklist/all/', '/api/*'
        ]
        self.development_ignore_paths = [
            '/test-add-users/', '/bulk-add-app-users/', '/test-login/', '/dev-add-bulk/'
        ]

    def should_ignore(self, path):
        return any(
            fnmatch(path, ignore_path) if '*' in ignore_path
            else path == ignore_path
            for ignore_path in self.ignore_paths
        )

    def __call__(self, request):
        self.count += 1
        print(f"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\nRequest #{self.count} - {request.path}\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

        if self.should_ignore(request.path) or request.path in self.development_ignore_paths:
            return self.get_response(request)
        else:
            response, continue_on = self.refresh_access_token(request)
            if continue_on:
                if response == "Access Token is still valid":
                    print(f"\nresponse: {response}\n")
                    response = self.get_response(request)
                else:
                    print(f"Token Refresh Success: {response}")
                    try:
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {response}'
                        print(f"New Authorization Header created: {request.META['HTTP_AUTHORIZATION']}")
                        request.META['X-Token-Refreshed'] = 'true'
                        print(f"New Header created: {request.META['X-Token-Refreshed']}")
                        response = self.get_response(request)
                    except Exception as e:
                        print(f"Error creating header in success: {e}")
                        response = HttpResponse({"ERROR:": e}, status=401)
            else:
                print(f"Token Refresh Error: {response}")
                try:
                    request.META['X-Token-Refreshed'] = 'false'
                    print(f"New Header created: {request.META['X-Token-Refreshed']}")
                except Exception as e:
                    print(f"Error creating header in failed: {e}")
                response = HttpResponse({f"{response}"}, status=401)
        response = self.process_response(request, response)
        return response

    def refresh_access_token(self, request):
        try:
            access_token = request.META.get('HTTP_AUTHORIZATION', None)
            refresh_token = request.META.get('HTTP_REFRESH_TOKEN', None)
            if refresh_token:
                not_blacklisted = self.token_generator.check_blacklist(refresh_token)
                if not_blacklisted is False:
                    return "ERROR in Refresh Access Token: Refresh Token is blacklisted", False
                if not_blacklisted is None:
                    return "ERROR in Refresh Access Token: Refresh Token is invalid", False
                token_valid = self.token_generator.validate_token(refresh_token)
                if not token_valid:
                    print(f"Refresh Token is expired")
                    return "ERROR in Refresh Access Token: Refresh Token has expired", False
            else:
                print(f"No refresh token")
                return "No refresh token", False
            if access_token:
                not_blacklisted = self.token_generator.check_blacklist(access_token, "access")
                if not_blacklisted is False:
                    print(f"Access Token is blacklisted")
                    return "ERROR: Token is blacklisted", False
                if not_blacklisted is None:
                    print(f"Access Token is invalid")
                    return "ERROR: Token is invalid", False
                token_expired = self.token_generator.is_token_expired(access_token)
                if token_expired:
                    print(f"Access Token is expired")
                    access_token = self.token_generator.refresh_access_token(refresh_token)
                    if access_token:
                        print("Token Refreshed")
                        return access_token, True
                    else:
                        print("Invalid Access token")
                        return "ERROR: Invalid Access token", False
                else:
                    print("Access Token is still valid")
                    return "Access Token is still valid", True
            else:
                print(f"No access token")
                return "No access token", False
        except Exception as e:
            print(f'Error: {e}')
            return f"ERROR: {e}", False

    def process_response(self, request, response):
        print(f"\n++++++++++++++\nResponse #{self.count} - {response.status_code}\n++++++++++++++++\n")
        return response
