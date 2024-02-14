#!/usr/bin/env python3
"""SessionAuth module

Classes:
    SessionAuth
"""
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """SessionAuth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id"""

        if user_id is None:
            return None

        if type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user id for a given session ID"""

        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns current user based on a cookie value"""

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        try:
            return User.get(user_id)
        except KeyError:
            return None

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session"""

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
