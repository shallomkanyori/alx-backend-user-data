#!/usr/bin/env python3
"""BasicAuth module

Classes:
    BasicAuth
"""
from .auth import Auth
import base64

from models.user import User

from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header"""

        if authorization_header is None:
            return None

        if type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of a Base64 string"""

        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header) is not str:
            return None

        try:
            return (base64.b64decode(base64_authorization_header)
                          .decode('utf-8'))
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Returns the user email and password from a Base64 decoded value.

        Assumes user email and password are separated by a ':' with only one
        ':' in the decoded value.
        """

        if decoded_base64_authorization_header is None:
            return (None, None)

        if type(decoded_base64_authorization_header) is not str:
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns a User instance based on their email and password."""

        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({"email": user_email})

            if users is None or len(users) == 0:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves a User instance for a request."""

        auth_header = self.authorization_header(request)
        auth_header_b64 = self.extract_base64_authorization_header(auth_header)
        ah_decoded = self.decode_base64_authorization_header(auth_header_b64)

        credentials = self.extract_user_credentials(ah_decoded)
        user = self.user_object_from_credentials(credentials[0],
                                                 credentials[1])

        return user
