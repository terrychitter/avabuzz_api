import os
from typing import Tuple
from config import Config
from functools import wraps
from app.services.jwt import jwt
from app.types.enum import UserType
from flask_jwt_extended import get_jwt
from app.services.auth.login import login
from app.services.auth.logout import logout
from flask import Response, request, jsonify
from app.services.auth.refresh_token import refresh_token
from app.services.auth.is_token_in_blocklist import is_token_in_blocklist

# JWT TOKEN IN BLOCKLIST LOADER
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return check_if_token_in_blocklist_service(jwt_header, jwt_payload)

# ----------------- CHECK IF TOKEN IN BLOCK LIST ------- #
def check_if_token_in_blocklist_service(jwt_header, jwt_payload):
    """
    Checks if a token is in the blocklist.

    This function checks if a token is in the blocklist.

    Args:
        jwt_header (Dict[str, str]): The JWT header.
        jwt_payload (Dict[str, str]): The JWT payload.

    Returns:
        bool: True if the token is in the blocklist, False otherwise.
    """
    return is_token_in_blocklist(jwt_payload["jti"])

# ----------------- API KEY REQUIRED ----------------- #
def api_key_required(f):
    """
    Decorator to check for the presence of a valid API key in the request headers

    Args:
        f (function): The function to decorate

    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key != Config.API_KEY:
            return jsonify({"message": "Forbidden or Invalid API key"}), 403
        return f(*args, **kwargs)

    return decorated_function

# ----------------- ADMIN REQUIRED ----------------- #
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = get_jwt().get("role")
        if role != UserType.ADMIN.value:
            return jsonify({"message": f"You do not have permission to access this resource."}), 403    
        return f(*args, **kwargs)
    return decorated_function

# ----------------- MODERATOR REQUIRED ----------------- #
def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = get_jwt().get("role")
        if role != UserType.MODERATOR.value and role != UserType.ADMIN.value:
            return jsonify({"message": f"You do not have permission to access this resource. Role {role}"}), 403    
        return f(*args, **kwargs)
    return decorated_function


# ----------------- LOGIN USER ----------------- #
def login_service(login_data: dict) -> Tuple[Response, int]:
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
    return login(login_data)

# ----------------- LOGOUT USER ----------------- #
def logout_service(jti: str) -> Tuple[Response, int]:
    """
    Logs out a user.

    This function adds the user's JWT token to the blocklist.

    Args:
        jti (str): The JWT ID of the token to be added to the blocklist.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the logout is successful, returns a JSON response with a message and a 200 status code.
            - If an error occurs during the logout process, returns a JSON response with an error message and a 500 status code
    """
    return logout(jti)

# ----------------- REFRESH TOKEN ----------------- #
def refresh_token_service(identity: str) -> Tuple[Response, int]:
    """
    Refreshes the user's access token.

    This function generates a new access token for the user.

    Args:
        identity (str): The user's private user ID.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the refresh is successful, returns a JSON response with a new access token and a 200 status code.
            - If an error occurs during the refresh process, returns a JSON response with an error message and a 500 status code
    """
    return refresh_token(identity)




