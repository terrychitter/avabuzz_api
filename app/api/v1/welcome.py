from flask import Blueprint, jsonify
from app.services.auth import api_key_required

bp = Blueprint("welcome", __name__)


@bp.route("/", methods=["GET"])
@api_key_required
def welcome():
    return jsonify({"message": "Welcome to the Avabuzz API"}), 200
