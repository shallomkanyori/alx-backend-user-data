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
        """To be implemented"""
        return False

    def authorization_header(self, request=None) -> str:
        """To be implemented"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """To be implemented"""
        return None
