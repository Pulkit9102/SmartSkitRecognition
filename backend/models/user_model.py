import re
from datetime import datetime, timezone

import bcrypt
from pymongo.errors import DuplicateKeyError, PyMongoError

from config.db import get_db

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class UserModel:
    collection_name = "users"

    @staticmethod
    def _collection():
        db = get_db()
        if db is None:
            return None
        return db[UserModel.collection_name]

    @staticmethod
    def validate_signup_payload(payload):
        name = (payload.get("name") or "").strip()
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password") or ""

        if not name:
            return False, "Name is required", None

        if len(name) < 2:
            return False, "Name must be at least 2 characters", None

        if not email:
            return False, "Email is required", None

        if not EMAIL_PATTERN.match(email):
            return False, "Invalid email format", None

        if not password:
            return False, "Password is required", None

        if len(password) < 6:
            return False, "Password must be at least 6 characters", None

        return True, None, {"name": name, "email": email, "password": password}

    @staticmethod
    def validate_login_payload(payload):
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password") or ""

        if not email or not password:
            return False, "Email and password are required", None

        if not EMAIL_PATTERN.match(email):
            return False, "Invalid email format", None

        return True, None, {"email": email, "password": password}

    @staticmethod
    def create_user(name, email, plain_password):
        collection = UserModel._collection()
        if collection is None:
            return None, "Database connection is not available"

        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())

        user_doc = {
            "name": name,
            "email": email,
            "password": hashed_password.decode("utf-8"),
            "createdAt": datetime.now(timezone.utc),
        }

        try:
            result = collection.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            return user_doc, None
        except DuplicateKeyError:
            return None, "User with this email already exists"
        except PyMongoError as exc:
            return None, f"Database error: {str(exc)}"

    @staticmethod
    def find_by_email(email):
        collection = UserModel._collection()
        if collection is None:
            return None

        return collection.find_one({"email": email.strip().lower()})

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def to_public_user(user_doc):
        return {
            "id": str(user_doc.get("_id")),
            "name": user_doc.get("name"),
            "email": user_doc.get("email"),
            "createdAt": user_doc.get("createdAt").isoformat()
            if user_doc.get("createdAt")
            else None,
        }
