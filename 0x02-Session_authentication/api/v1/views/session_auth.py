#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Login to user session
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})

        if users is None or len(users) == 0:
            return jsonify({"error": "no user found for this email"}), 404

        user = None
        for u in users:
            if u.is_valid_password(password):
                user = u
                break

        if user is None:
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        session_name = os.getenv("SESSION_NAME")

        response = jsonify(user.to_json())
        response.set_cookie(session_name, session_id)

        return response

    except KeyError:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Logout from user session
    """

    from api.v1.app import auth
    success = auth.destroy_session(request)

    if not success:
        abort(404)

    return jsonify({}), 200
