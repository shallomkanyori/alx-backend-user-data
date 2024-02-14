#!/usr/bin/env python3
"""SessionExpAuth module

Classes:
    SessionExpAuth
"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        super().__init__()

        duration = os.getenv("SESSION_DURATION", 0)
        try:
            duration = int(duration)
        except ValueError:
            duration = 0

        self.session_duration = duration

    def create_session(self, user_id=None):
        """Creates a session for a user_id"""

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {"user_id": user_id,
                                                  "created_at": datetime.now()}

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user id for a given session id"""

        if session_id is None:
            return None

        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None

        if self.session_duration <= 0:
            return session["user_id"]

        if session.get("created_at") is None:
            return None

        if (session["created_at"] + timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None

        return session["user_id"]
