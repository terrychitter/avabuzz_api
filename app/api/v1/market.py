from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app.services.auth import api_key_required, admin_required
from app.services.market import get_profile_accessories_service, create_profile_accessories_service, update_profile_accessories_service, delete_profile_accessories_service

bp = Blueprint("market", __name__)

# ----------------- GET ALL MARKET ITEMS ----------------- #
@bp.route("/market/profile-accessories", methods=["GET"])
@api_key_required
@jwt_required()
def get_market_items():
    return get_profile_accessories_service()

# ----------------- CREATE MARKET ITEM ----------------- #
@bp.route("/market/profile-accessories", methods=["POST"])
@api_key_required
@jwt_required()
@admin_required
def create_market_item():
    return create_profile_accessories_service()

# ----------------- UPDATE MARKET ITEM ----------------- #
@bp.route("/market/profile-accessories/<string:item_id>", methods=["PUT"])
@api_key_required
@jwt_required()
@admin_required
def update_market_item(item_id):
    return update_profile_accessories_service(item_id=item_id)

# ----------------- DELETE MARKET ITEM ----------------- #
@bp.route("/market/profile-accessories/<string:item_id>", methods=["DELETE"])
@api_key_required
@jwt_required()
@admin_required
def delete_market_item(item_id):
    return delete_profile_accessories_service(item_id=item_id)