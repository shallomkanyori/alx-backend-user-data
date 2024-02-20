#!/usr/bin/env python3
"""End-to-end intergration test"""
import requests


def register_user(email: str, password: str) -> None:
    """Tests registering a user"""

    url = "http://localhost:5000/users"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200

    rj = response.json()
    assert rj["email"] == email
    assert rj["message"] == "user created"


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests logging in with a wrong password"""

    url = "http://localhost:5000/sessions"
    response = requests.post(url, data={"email": email, "password": password})

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests logging in"""

    url = "http://localhost:5000/sessions"
    response = requests.post(url, data={"email": email, "password": password})

    assert response.status_code == 200

    rj = response.json()
    assert rj["email"] == email
    assert rj["message"] == "logged in"

    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Tests the /profile route without logging in"""

    url = "http://localhost:5000/profile"
    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests the /profile route after logging in"""

    url = "http://localhost:5000/profile"
    response = requests.get(url, cookies={"session_id": session_id})

    assert response.status_code == 200

    rj = response.json()
    assert rj["email"] is not None


def log_out(session_id: str) -> None:
    """Tests logging out"""

    url = "http://localhost:5000/sessions"
    response = requests.delete(url, cookies={"session_id": session_id})

    # assert that we were redirected to GET /
    assert response.status_code == 200

    rj = response.json()
    assert rj["message"] == "Bienvenue"


def reset_password_token(email: str) -> str:
    """Tests getting a password reset token"""

    url = "http://localhost:5000/reset_password"
    response = requests.post(url, data={"email": email})

    assert response.status_code == 200

    rj = response.json()
    assert rj["email"] == email
    assert rj["reset_token"] is not None

    return rj["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating a password"""

    url = "http://localhost:5000/reset_password"
    payload = {"email": email,
               "reset_token": reset_token,
               "new_password": new_password}

    response = requests.put(url, data=payload)

    assert response.status_code == 200

    rj = response.json()
    assert rj["email"] == email
    assert rj["message"] == "Password updated"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
