from app import db
from flask import Blueprint, app, request
from app.services.auth import api_key_required
from app.services.login import login_service

bp = Blueprint("login", __name__)

@bp.route("/login", methods=["POST"])
@api_key_required
def login():
    data = request.get_json()
    return login_service(data) 
