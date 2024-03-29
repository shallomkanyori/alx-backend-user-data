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
from typing import Union


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

    def create_session(self, email: str) -> str:
        """Creates new session and returns its ID"""

        try:
            user = self._db.find_user_by(**{"email": email})
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, **{"session_id": session_id})

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Returns the user with the given session_id"""

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(**{"session_id": session_id})
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session for a given user"""

        self._db.update_user(user_id, **{"session_id": None})

    def get_reset_password_token(self, email: str) -> str:
        """Returns a password reset token for user with a given email"""

        try:
            user = self._db.find_user_by(**{"email": email})
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, **{"reset_token": reset_token})

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Resets/updates a user's password"""

        try:
            user = self._db.find_user_by(**{"reset_token": reset_token})
        except NoResultFound:
            raise ValueError

        pwd_hash = _hash_password(password)
        self._db.update_user(user.id, **{"hashed_password": pwd_hash,
                                         "reset_token": None})
