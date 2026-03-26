import os
from functools import wraps

import jwt
from flask import g, jsonify, request


def require_auth(handler):
    """Decorator to protect optional future routes with JWT auth."""

    @wraps(handler)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "error": "Missing Bearer token"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        secret = os.getenv("JWT_SECRET", "")

        if not secret:
            return jsonify({"success": False, "error": "JWT_SECRET is not configured"}), 500

        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            g.auth_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "error": "Invalid token"}), 401

        return handler(*args, **kwargs)

    return wrapped
