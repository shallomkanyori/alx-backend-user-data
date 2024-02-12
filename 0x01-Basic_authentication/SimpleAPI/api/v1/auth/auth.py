#!/usr/bin/env python3
"""Auth module

Classes:
    Auth
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authorization.

        Args:
            path (str): the path to check.
            excluded_paths (list of str): paths that don't need authorization
                                          (end-slash tolerant).
        """

        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path in excluded_paths or (path + '/') in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from a request."""

        if request is None:
            return None

        auth_header = request.headers.get('Authorization')

        if auth_header:
            return auth_header

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """To be implemented"""
        return None
