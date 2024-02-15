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

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session = UserSession(**{"user_id": user_id,
                                 "session_id": session_id})
        session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user id for a given session id"""

        if session_id is None:
            return None

        try:
            sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None

        if len(sessions) <= 0:
            return None

        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        if session.created_at is None:
            return None

        if (session.created_at + timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None

        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Destorys a user session based on the session id."""

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return False

        if len(sessions) <= 0:
            return False

        sessions[0].remove()

        return True
