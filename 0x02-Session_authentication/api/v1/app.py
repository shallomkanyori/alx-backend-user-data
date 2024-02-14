#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE", "") == "session_exp_auth":
    auth = SessionExpAuth()
elif getenv("AUTH_TYPE", "") == "session_auth":
    auth = SessionAuth()
elif getenv("AUTH_TYPE", "") == "basic_auth":
    auth = BasicAuth()
elif getenv("AUTH_TYPE", "") == "auth":
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def un_authoried(error) -> str:
    """ Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """Filters requests for authorization."""

    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    curr_user = auth.current_user(request)
    if curr_user is None:
        abort(403)

    request.current_user = curr_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
