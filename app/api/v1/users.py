from app import db
from datetime import datetime
from app.models.users import Users
from flask import Blueprint, jsonify, request
from app.services.auth import api_key_required
from app.services.users import create_user_service, get_users_service, delete_user_service, update_user_service

bp = Blueprint("users", __name__)


# ----------------- GET ALL USERS ----------------- #
@bp.route("/users", methods=["GET"])
@api_key_required
def get_users():
    return get_users_service()


# ----------------- GET USER BY PUBLIC ID ----------------- #
@bp.route("/users/<string:public_user_id>", methods=["GET"])
@api_key_required
def get_user(public_user_id):
    return get_users_service(public_user_id)
    

# ----------------- CREATE USER ----------------- #
@bp.route("/users", methods=["POST"])
@api_key_required
def create_user():
    # Extract user data from the request body
    user_data = request.get_json()
    return create_user_service(user_data)

# ----------------- UPDATE USER ----------------- #
@bp.route("/users/<string:public_user_id>", methods=["PUT"])
@api_key_required
def update_user(public_user_id):
    # Extract user data from the request body
    user_data = request.get_json()
    return update_user_service(public_user_id, user_data)

# ----------------- DELETE USER ----------------- #
@bp.route("/users/<string:public_user_id>", methods=["DELETE"])
@api_key_required
def delete_user(public_user_id):
    return delete_user_service(public_user_id)
