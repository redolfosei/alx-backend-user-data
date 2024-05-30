#!/usr/bin/env python3
"""module docs for app.py"""
from flask import (
    Flask, Response, abort, jsonify, redirect, request, make_response, url_for)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> Response:
    """root url"""
    message = {"message": "Bienvenue"}
    return jsonify(message), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """register a new user"""
    credentials = request.form
    if 'email' not in credentials or\
            'password' not in credentials:
        return
    try:
        new_user = AUTH.register_user(credentials.get(
            'email'), credentials.get('password'))
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    # print(new_user.hashed_password)
    return jsonify({
        "email": f"{new_user.email}", "message": "user created"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """login handler"""
    credentials = request.form
    if 'email' not in credentials or\
            'password' not in credentials:
        abort(401)
    email = credentials.get("email")
    password = credentials.get("password")
    valid = AUTH.valid_login(email, password)
    if valid:
        session_id = AUTH.create_session(email)
        response = make_response({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response, 200
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """destroys and logout a user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """returns a user profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """reset password token endpoint"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """reset user's password endpoint"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if email is None or reset_token is None or new_password is None:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
