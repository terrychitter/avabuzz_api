from app import db
from flask import Blueprint, request
from app.services.auth import api_key_required
from app.services.posts import get_posts_service, create_post_service, delete_post_service

bp = Blueprint("posts", __name__)


# ----------------- GET ALL POSTS ----------------- #
@bp.route("/posts", methods=["GET"])
@api_key_required
def get_posts():
    return get_posts_service()

# ----------------- GET POST BY ID ----------------- #
@bp.route("/posts/<int:post_id>", methods=["GET"])
@api_key_required
def get_post_by_id(post_id):
    return get_posts_service(post_id=post_id)

# ----------------- CREATE NEW POST ----------------- #
@bp.route("/posts", methods=["POST"])
@api_key_required
def create_post():
    data = request.get_json()
    # Perform validation and create new post
    return create_post_service(data)

# ----------------- DELETE POST ----------------- #
@bp.route("/posts/<int:post_id>", methods=["DELETE"])
@api_key_required
def delete_post(post_id):
    return delete_post_service(post_id)