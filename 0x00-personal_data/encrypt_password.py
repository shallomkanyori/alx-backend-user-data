#!/usr/bin/env python3
"""Personal data.
Encrypting passwords.

Functions:
    hash_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted and hashed password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
