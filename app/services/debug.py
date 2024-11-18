from datetime import datetime
from typing import Tuple
from flask import Response, jsonify
from app import db
from app.models import Users
from app.types.enum import ProfileAccessoryType, ProfileType, OwnershipType, UserType
from app.utils.id_generation import generate_uuid

def debug_service() -> Tuple[Response, int]:
    try:

        # Get a user
        user: Users = Users.query.filter_by(private_user_id="M3N8CJ41HS").first()

        user.user_type = UserType.ADMIN
        db.session.commit()

        return jsonify({"message": "Debug Successful!", "item": "is admin" if user.is_admin() else "not admin"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    