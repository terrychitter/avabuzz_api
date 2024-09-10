from app import db
from flask import Blueprint, app, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.services.auth import api_key_required, login_service, refresh_token_service, logout_service

bp = Blueprint("auth", __name__)

# ----------------- LOGIN USER ----------------- #
@bp.route("/login", methods=["POST"])
@api_key_required
def login():
    data = request.get_json()
    return login_service(data)

# ----------------- LOGOUT USER ----------------- #
@bp.route("/logout", methods=["POST"])
@api_key_required
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    return logout_service(jti)

# ----------------- REFRESH TOKEN ----------------- #
@bp.route("/refresh", methods=["POST"])
@api_key_required
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return refresh_token_service(identity)
