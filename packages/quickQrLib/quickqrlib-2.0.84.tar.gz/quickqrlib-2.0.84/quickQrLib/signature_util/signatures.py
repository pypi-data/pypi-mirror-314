from django.conf import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json
import base64
import logging
from django.http import HttpResponse
from typing import List, Dict
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)

try:
    private_key = serialization.load_pem_private_key(
        settings.PRIVATE_KEY,
        password=None,
        backend=default_backend()
    )
except Exception as e:
    logger.error(f"Error loading private key:'{e}'")

class SignatureActions:
    '''Where permissions are a dictionary of permissions'''
    @classmethod
    def sign_permissions(cls, permissions)->List[Dict]:
        signed_permissions = []
        msg = ""
        status_code = status.HTTP_100_CONTINUE
        try:
            private_key = serialization.load_pem_private_key(
                settings.PRIVATE_KEY,
                password=None,
                backend=default_backend()
            )
            if permissions:
                for permission in permissions:
                    json_permission = json.dumps(permission, default=str)
                    signature = private_key.sign(
                        json_permission.encode('utf-8'),
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    permission["signature"] = base64.b64encode(signature).decode('utf-8')
                    signed_permissions.append(permission)
            else:
                msg = "No permissions to sign"
                status_code = status.HTTP_400_BAD_REQUEST
                return msg, status_code, False
        except Exception as e:
            # Handle the exception (log, raise, etc.)
            print(f"Error signing permissions: {e}")
            logger.error(f"Error signing permissions: '{type(e).__name__}'")
            msg = "Error signing permissions"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return msg, status_code, False
        status_code = status.HTTP_200_OK
        return signed_permissions, status_code, True

    @classmethod
    def verify_header_permissions(cls, permission, signature) -> dict:
        json_permission = {}
        if permission and signature:
            public_key = serialization.load_pem_public_key(
                settings.PUBLIC_KEY,
                backend=default_backend()
            )
            signature_bytes = base64.b64decode(signature)
            try:
                json_permission= json.loads(permission)
                json_dumped_permission = json.dumps(json_permission, default=str)
                public_key.verify(
                    signature_bytes,
                    json_dumped_permission.encode('utf-8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
            except Exception as e:
                logger.error(f"Error verifying header permissions: '{type(e).__name__}'")
                return {}, {}
            if json_permission:
                return json_permission
        return {}

class SignatureCheckMixin:
    def __init__ (self, permission_type = 'model', *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        permission_result = self.is_signature_valid(request)
        #Returns permissions dictionary if valid, else empty dict
        if not permission_result:
            return HttpResponse('message: Invalid permissions', status=403)
        else:
            request.permission= permission_result
            return super().dispatch(request, *args, **kwargs)

    def is_signature_valid(self, request):
        # Check the signature
        permission = None
        signature = None

        if request.META.get('HTTP_PERMISSION'):
            permission = request.META.get('HTTP_PERMISSION')
            signature = request.META.get('HTTP_PERMISSION_SIGNATURE')

        return SignatureActions.verify_header_permissions(permission, signature)
