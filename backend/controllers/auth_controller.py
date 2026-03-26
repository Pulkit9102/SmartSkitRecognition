import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import jsonify, request

from config.db import get_db_error
from models.user_model import UserModel


def _jwt_secret():
    return os.getenv("JWT_SECRET", "")


def _jwt_expiry_minutes():
    try:
        return int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
    except ValueError:
        return 60


def _generate_token(user_doc):
    secret = _jwt_secret()
    if not secret:
        return None

    expiry_minutes = _jwt_expiry_minutes()
    now_utc = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_doc.get("_id")),
        "email": user_doc.get("email"),
        "name": user_doc.get("name"),
        "iat": int(now_utc.timestamp()),
        "exp": int((now_utc + timedelta(minutes=expiry_minutes)).timestamp()),
    }

    return jwt.encode(payload, secret, algorithm="HS256")


def signup():
    payload = request.get_json(silent=True) or {}

    is_valid, error, cleaned = UserModel.validate_signup_payload(payload)
    if not is_valid:
        return jsonify({"success": False, "error": error}), 400

    created_user, create_error = UserModel.create_user(
        cleaned["name"], cleaned["email"], cleaned["password"]
    )
    if create_error:
        status_code = 409 if "already exists" in create_error else 503
        return jsonify({"success": False, "error": create_error}), status_code

    token = _generate_token(created_user)
    if token is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "JWT_SECRET is not configured in environment",
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "success": True,
                "message": "User registered successfully",
                "token": token,
                "user": UserModel.to_public_user(created_user),
            }
        ),
        201,
    )


def login():
    payload = request.get_json(silent=True) or {}

    is_valid, error, cleaned = UserModel.validate_login_payload(payload)
    if not is_valid:
        return jsonify({"success": False, "error": error}), 400

    user_doc = UserModel.find_by_email(cleaned["email"])
    if not user_doc:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401

    is_password_valid = UserModel.verify_password(
        cleaned["password"], user_doc.get("password", "")
    )
    if not is_password_valid:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401

    token = _generate_token(user_doc)
    if token is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "JWT_SECRET is not configured in environment",
                }
            ),
            500,
        )

    return jsonify(
        {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": UserModel.to_public_user(user_doc),
        }
    )


def auth_health():
    db_error = get_db_error()
    return jsonify(
        {
            "success": True,
            "auth": "ready" if db_error is None else "degraded",
            "db_error": db_error,
            "jwt_configured": bool(_jwt_secret()),
        }
    )
