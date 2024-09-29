import datetime
from config import Config
from typing import Dict, Tuple
from flask import Response, jsonify
from app.models import Users
from werkzeug.security import check_password_hash
from app.utils.validation_utils import validate_required_fields
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

def login(login_data: Dict[str, str]) -> Tuple[Response, int]:
    """
    Logs in a user.

    This function performs the following tasks:
    - Validates the required fields for a login request.
    - Checks if the user exists.
    - Checks if the password matches.
    - Generates a JWT token for the user.

    Args:
        login_data (Dict[str, str]): A dictionary containing the email and password of the user.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the login is successful, returns a JSON response with an access token and a 200 status code.
            - If the email or password is incorrect, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during the login process, returns a JSON response with an error message and a 500 status code
    """
    try:
        # Define the required fields for a login request
        required_fields = [
            {"fields": ["email"], "message": "Email required."},
            {"fields": ["password"], "message": "Password required."}
        ]

        # Validate the required fields
        validation_message, status_code = validate_required_fields(login_data, required_fields)
        if status_code != 200:
            return validation_message, status_code
        
        # Check if the user exists
        user = Users.query.filter_by(email=login_data["email"]).first()
        if not user:
            return jsonify({"message": "Incorrect email or password."}), 401
        
        # Check if the password matches
        if not check_password_hash(user.password_hash, login_data["password"]):
            return jsonify({"message": "Incorrect email or password."}), 401 
        
        # Generate a JWT token
        access_token = create_access_token(identity=user.private_user_id)
        refresh_token = create_refresh_token(identity=user.private_user_id)

        return jsonify(
            {"access_token": access_token,
             "refresh_token": refresh_token,
             "access_token_expires": Config.JWT_ACCESS_TOKEN_EXPIRES,
             "refresh_expires" : Config.JWT_REFRESH_TOKEN_EXPIRES
             }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
