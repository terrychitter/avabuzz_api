from app import db
from flask import Blueprint, request
from app.services.auth import api_key_required
from app.services.users import (
    create_user_service,
    get_users_service,
    delete_user_service,
    update_user_service,
    follow_user_service,
    unfollow_user_service
    )

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

# ----------------- FOLLOW USER ----------------- #
@bp.route("/users/<string:followee_private_user_id>/follow", methods=["POST"])
@api_key_required
def follow_user(followee_private_user_id):
    # Extract the followers private_user_id from the request body
    follower_private_user_id = request.get_json().get("private_user_id")
    return follow_user_service(follower_private_user_id, followee_private_user_id)

# ----------------- UNFOLLOW USER ----------------- #
@bp.route("/users/<string:unfollowee_private_user_id>/unfollow", methods=["POST"])
@api_key_required
def unfollow_user(unfollowee_private_user_id):
    # Extract the followers private_user_id from the request body
    unfollower_private_user_id = request.get_json().get("private_user_id")
    return unfollow_user_service(unfollower_private_user_id, unfollowee_private_user_id)