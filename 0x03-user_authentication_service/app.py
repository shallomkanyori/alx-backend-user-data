#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Returns basic welcome payload"""

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Register a user"""

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)

        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Logs in a user"""

    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Logs out a user"""

    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destory_session(user.id)

        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Returns user's information"""

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """Generates a password reset token"""

    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)

        return jsonify({"email": email, "reset_token": reset_token})

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
