import os

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError

    PYMONGO_AVAILABLE = True
except Exception:
    MongoClient = None

    class PyMongoError(Exception):
        pass

    PYMONGO_AVAILABLE = False

_db_client = None
_db_instance = None
_db_error = None


def init_mongo_db():
    """Initialize MongoDB client once and cache DB reference."""
    global _db_client, _db_instance, _db_error

    if _db_instance is not None or _db_error is not None:
        return _db_instance

    mongo_uri = os.getenv("MONGODB_URI", "")
    db_name = os.getenv("MONGODB_DB_NAME", "skin_disease_app")

    if not PYMONGO_AVAILABLE:
        _db_error = "pymongo is not installed"
        return None

    if not mongo_uri:
        _db_error = "MONGODB_URI is not configured"
        return None

    try:
        _db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        _db_client.admin.command("ping")
        _db_instance = _db_client[db_name]
        _db_instance.users.create_index("email", unique=True)
        return _db_instance
    except PyMongoError as exc:
        _db_error = str(exc)
        _db_instance = None
        return None


def get_db():
    """Get MongoDB database object or None if unavailable."""
    if _db_instance is not None:
        return _db_instance
    return init_mongo_db()


def get_db_error():
    """Return initialization error string when DB is unavailable."""
    if _db_error is not None:
        return _db_error

    if _db_instance is None:
        init_mongo_db()

    return _db_error
