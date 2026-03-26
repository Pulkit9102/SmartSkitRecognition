from flask import Blueprint

from controllers.auth_controller import auth_health, login, signup

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

auth_bp.post("/signup")(signup)
auth_bp.post("/login")(login)
auth_bp.get("/health")(auth_health)
