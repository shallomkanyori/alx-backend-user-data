#!/usr/bin/env python3
"""Authentication module

Functions:
    _hash_password

Classes:
    Auth
"""
import bcrypt
from db import DB
from user import User

from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns hashed password"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers and returns a user"""

        try:
            self._db.find_user_by(**{"email": email})
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError("User {} already exists".format(email))
