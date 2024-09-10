from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.auth import api_key_required
from app.services.blocks import get_blocked_users_service, block_user_service, unblock_user_service

bp = Blueprint("blocks", __name__)

# ----------------- GET BLOCK LIST FOR USER ----------------- #
@bp.route("/blocks", methods=["GET"])
@api_key_required
@jwt_required()
def get_blocked_users():
    # Get private_user_id from JWT token
    private_user_id = get_jwt_identity()
    return get_blocked_users_service(private_user_id)


# ----------------- BLOCK USER ----------------- #
@bp.route("/blocks/<string:blocked_id>", methods=["POST"])
@api_key_required
@jwt_required()
def block_user(blocked_id: str):
    # Get blocker ID from JWT token
    blocker_id = get_jwt_identity()
    return block_user_service(blocker_id, blocked_id)

# ----------------- UNBLOCK USER ----------------- #
@bp.route("/blocks/<string:unblocked_id>", methods=["DELETE"])
@api_key_required
@jwt_required()
def unblock_user(unblocked_id: str):
    # Get unblocker ID from JWT token
    unblocker_id = get_jwt_identity()
    return unblock_user_service(unblocker_id, unblocked_id)