from app import db
from flask import Blueprint, jsonify

from app.services.debug import debug_service

bp = Blueprint("debug", __name__)

@bp.route("/debug", methods=["POST"])
def debug():
    return debug_service()