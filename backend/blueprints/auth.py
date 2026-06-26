from flask import Blueprint, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


@auth_bp.route("/login", methods=["POST"])
def login():
    conn, cursor = get_db()
    username = request.form.get("username")
    password = request.form.get("password")
    if not (username and password):
        return jsonify({"error": "username and password are required"}), 400

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user is None or not check_password_hash(user["user_password"], password):
        return jsonify({"error": "username or password is incorrect"}), 400

    session.clear()
    session["user_id"] = user["user_id"]
    session["username"] = user["username"]
    session["type"] = user["user_type"]
    return jsonify({"user_type": user["user_type"], "username": user["username"]}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    conn, cursor = get_db()
    username = request.form.get("username")
    password = request.form.get("password")
    conf_pass = request.form.get("confirm_password")
    org = request.form.get("user_org")

    if not (username and password and conf_pass):
        return jsonify({"error": "username and password are required"}), 400
    if password != conf_pass:
        return jsonify({"error": "your password and confirm password do not match"}), 400

    cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({"error": "username is taken"}), 400

    # Self-registration always creates a student. Admins are seeded separately.
    cursor.execute(
        """INSERT INTO users (username, user_password, user_type, user_org, user_status)
           VALUES (%s, %s, 'student', %s, 1)""",
        (username, generate_password_hash(password, method="pbkdf2:sha256"), org),
    )
    conn.commit()
    return jsonify({"success": "user has been registered"}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": "logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    """Return the current session user, or 401 if not logged in."""
    if session.get("user_id") is None:
        return jsonify({"error": "not authenticated"}), 401
    return jsonify({
        "user_id": session["user_id"],
        "username": session.get("username"),
        "user_type": session.get("type"),
    }), 200
