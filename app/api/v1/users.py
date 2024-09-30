from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from flask import Blueprint, request
from app.services.auth import api_key_required
from app.services.posts import get_posts_for_user_service
from app.services.users import (
    create_user_service,
    get_users_service,
    get_me_service,
    delete_user_service,
    update_user_service,
    get_user_followers_service,
    get_user_following_service,
    follow_user_service,
    unfollow_user_service
    )

bp = Blueprint("users", __name__)


# ----------------- GET ALL USERS ----------------- #
@bp.route("/users", methods=["GET"])
@api_key_required
def get_users():
    return get_users_service()

# ----------------- GET LOGGED IN USER ----------------- #
@bp.route("/users/me", methods=["GET"])
@api_key_required
@jwt_required()
def get_logged_in_user():
    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()
    return get_me_service(private_user_id)


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
@bp.route("/users", methods=["PUT"])
@api_key_required
@jwt_required()
def update_user():
    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()

    # Extract user data from the request body
    user_data = request.get_json()
    return update_user_service(private_user_id, user_data)

# ----------------- DELETE USER ----------------- #
@bp.route("/users", methods=["DELETE"])
@api_key_required
@jwt_required()
def delete_user(private_user_id):
    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()
    
    return delete_user_service(private_user_id)

# ----------------- GET POSTS BY PUBLIC_USER_ID ----------------- #
@bp.route("users/<string:public_user_id>/posts", methods=["GET"])
@api_key_required
def get_posts_by_user(public_user_id):
    return get_posts_for_user_service(public_user_id)

# ----------------- GET USER FOLLOWERS ----------------- #
@bp.route("/users/<string:public_user_id>/followers", methods=["GET"])
@api_key_required
def get_user_followers(public_user_id):
    return get_user_followers_service(public_user_id)

# ----------------- GET USER FOLLOWING ----------------- #
@bp.route("/users/<string:public_user_id>/following", methods=["GET"])
@api_key_required
def get_user_following(public_user_id):
    return get_user_following_service(public_user_id)

# ----------------- FOLLOW USER ----------------- #
@bp.route("/users/<string:followee_public_user_id>/follow", methods=["POST"])
@api_key_required
@jwt_required()
def follow_user(followee_public_user_id):
    # Get the follower's private_user_id from the JWT
    follower_private_user_id = get_jwt_identity()
    return follow_user_service(follower_private_user_id, followee_public_user_id)

# ----------------- UNFOLLOW USER ----------------- #
@bp.route("/users/<string:unfollowee_public_user_id>/unfollow", methods=["POST"])
@api_key_required
@jwt_required()
def unfollow_user(unfollowee_public_user_id):
    # Extract the followers private_user_id from the JWT
    unfollower_private_user_id = get_jwt_identity()
    return unfollow_user_service(unfollower_private_user_id, unfollowee_public_user_id)