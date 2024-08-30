from app import db
from flask import Blueprint, request
from app.services.auth import api_key_required
from app.services.hashtags import (
    get_hashtags_service,
    get_posts_for_hashtag_service
)

bp = Blueprint("hashtags", __name__)


# ----------------- GET ALL HASHTAGS ----------------- #
@bp.route("/hashtags", methods=["GET"])
@api_key_required
def get_hashtags():
    return get_hashtags_service()

# ----------------- GET SPECIFIC HASHTAG ----------------- #
@bp.route("/hashtags/<hashtag_name>", methods=["GET"])
@api_key_required
def get_specific_hashtag(hashtag_name):
    return get_hashtags_service(hashtag_name)

# ----------------- GET POSTS FOR HASHTAG ----------------- #
@bp.route("/hashtags/<hashtag_name>/posts", methods=["GET"])
@api_key_required
def get_posts_for_hashtag(hashtag_name):
    return get_posts_for_hashtag_service(hashtag_name)