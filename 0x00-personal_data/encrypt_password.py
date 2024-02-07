#!/usr/bin/env python3
"""Personal data.

Encrypts passwords.
Checks if a password is valid.

Functions:
    hash_password(password)
    is_valid(hashed_password, password)
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted and hashed password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
