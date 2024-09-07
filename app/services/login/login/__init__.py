from typing import Dict, Tuple
from flask import Response, jsonify
from app.models import Users
from werkzeug.security import check_password_hash
from app.utils.validation_utils import validate_required_fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def login(login_data: Dict[str, str]) -> Tuple[Response, int]:
    try:
        # Define the required fields for a login request
        required_fields = [
            {"fields": ["email"], "message": "Email required."},
            {"fields": ["password"], "message": "Password required."}
        ]

        # Validate the required fields
        validation_error, status_code = validate_required_fields(login_data, required_fields)
        if validation_error:
            return validation_error, status_code
        
        # Check if the user exists
        user = Users.query.filter_by(email=login_data["email"]).first()
        if not user:
            return jsonify({"message": "Invalid email or password."}), 404
        
        # Check if the password matches
        if not check_password_hash(user.password_hash, login_data["password"]):
            return jsonify({"message": "Invalid email or password."}), 400 
        
        # Generate a JWT token
        access_token = create_access_token(identity=user.private_user_id, expires_delta=False)

        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
