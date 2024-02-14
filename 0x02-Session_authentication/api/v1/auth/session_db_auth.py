#!/usr/bin/env python3
"""SessionDBAuth module

Classes:
    SessionDBAuth
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Creates a session for a user_id"""

        session = UserSession(**{"user_id": user_id})
        session.save()

        return session.id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user id for a given session id"""

        if session_id is None:
            return None

        session = UserSession.get(session_id)
        if session is None:
            return None

        if self.session_duration <= 0:
            return session.user_id

        if session.created_at is None:
            return None

        if (session.created_at + timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """Destorys a user session based on the session id."""

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        sessions = UserSession.get(session_id)
        if session is None:
            return False

        UserSession.remove(session.id)

        return True
