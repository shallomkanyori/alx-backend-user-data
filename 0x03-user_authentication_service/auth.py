#!/usr/bin/env python3
"""Authentication module

Functions:
    _hash_password
    _generate_uuid

Classes:
    Auth
"""
import bcrypt
import uuid

from db import DB
from user import User

from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns hashed password"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns new UUID as a string"""

    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials"""

        try:
            user = self._db.find_user_by(**{"email": email})
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode(), user.hashed_password)
