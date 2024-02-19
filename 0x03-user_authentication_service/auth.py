#!/usr/bin/env python3
"""Authentication module

Functions:
    _hash_password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns hashed password"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
