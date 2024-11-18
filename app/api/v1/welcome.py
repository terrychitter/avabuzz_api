from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app.services.auth import api_key_required, admin_required

bp = Blueprint("welcome", __name__)


@bp.route("/", methods=["GET"])
@api_key_required
@jwt_required()
@admin_required
def welcome():
    return jsonify({"message": "Welcome to the Avabuzz API"})
