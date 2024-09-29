from flask import jsonify, Response
from typing import Tuple
from app.models import Users

def get_me(private_user_id: str) -> Tuple[Response, int]:
    try:
        # Check if the user exists
        user = Users.query.filter_by(private_user_id=private_user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Return the user data
        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500