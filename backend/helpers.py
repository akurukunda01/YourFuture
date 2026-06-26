from functools import wraps

from flask import jsonify, session


def login_required(f):
    """Require an authenticated session; respond 401 (JSON) otherwise."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return jsonify({"error": "authentication required"}), 401
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Require an authenticated admin session; respond 401/403 otherwise."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return jsonify({"error": "authentication required"}), 401
        if session.get("type") != "admin":
            return jsonify({"error": "admin access required"}), 403
        return f(*args, **kwargs)

    return decorated_function
