from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from app import db
from flask import Blueprint, request
from app.services.auth import api_key_required
from app.services.posts import (
    get_posts_service,
    create_post_service,
    delete_post_service,
    get_posts_for_user_service,
    react_to_post_service,
    unreact_to_post_service
)

bp = Blueprint("posts", __name__)


# ----------------- GET ALL POSTS ----------------- #
@bp.route("/posts", methods=["GET"])
@api_key_required
def get_posts():
    try:
        verify_jwt_in_request()
        private_user_id = get_jwt_identity()
        return get_posts_service(post_id=None, private_user_id=private_user_id)
    except:
        return get_posts_service(None, None)

# ----------------- GET POST BY ID ----------------- #
@bp.route("/posts/<int:post_id>", methods=["GET"])
@api_key_required
def get_post_by_id(post_id):
    try:
        verify_jwt_in_request()
        private_user_id = get_jwt_identity()
        return get_posts_service(post_id=post_id, private_user_id=private_user_id)
    except:
        return get_posts_service(post_id=post_id, private_user_id=None)

# ----------------- CREATE NEW POST ----------------- #
@bp.route("/posts", methods=["POST"])
@api_key_required
@jwt_required()
def create_post():
    # Extract post data from the request body
    post_data = request.get_json()

    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()
    return create_post_service(private_user_id, post_data)

# ----------------- DELETE POST ----------------- #
@bp.route("/posts/<int:post_id>", methods=["DELETE"])
@api_key_required
@jwt_required()
def delete_post(post_id):
    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()
    return delete_post_service(private_user_id, post_id)

# ----------------- GET POSTS BY PUBLIC_USER_ID ----------------- #
@bp.route("/posts/<string:public_user_id>", methods=["GET"])
@api_key_required
def get_posts_by_user(public_user_id):
    return get_posts_for_user_service(public_user_id)

# ----------------- REACT TO POST ----------------- #
@bp.route("/posts/<int:post_id>/react/<string:reaction>", methods=["POST"])
@api_key_required
@jwt_required()
def react_to_post(post_id, reaction):
    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()
    return react_to_post_service(private_user_id, post_id, reaction)

# ----------------- UNREACT TO POST ----------------- #
@bp.route("/posts/<int:post_id>/react", methods=["DELETE"])
@api_key_required
@jwt_required()
def unreact_to_post(post_id):
    # Get the user's private_user_id from the JWT
    private_user_id = get_jwt_identity()
    return unreact_to_post_service(private_user_id, post_id)