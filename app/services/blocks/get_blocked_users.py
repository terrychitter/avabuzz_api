from typing import Tuple
from flask import Response, jsonify
from app.models import Users, BlockedUsers

def get_blocked_users(private_user_id: str) -> Tuple[Response, int]:
    """
    Get the list of users blocked by the user.

    This function performs the following tasks:
    - Checks if the user exists.
    - Retrieves the list of blocked users.
    - Returns the list of blocked users.

    Args:
        private_user_id (str): The private user ID of the user.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the user is found, returns a JSON response with the list of blocked users and a 200 status code.
            - If the user is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during the process, returns a JSON response with an error message and a 500 status code.
    """
    try:
        # Check if the user exists
        user = Users.query.filter_by(private_user_id=private_user_id).first()
        if not user:
            return jsonify({"message": "User not found."}), 404
        
        # Get the list of blocked users
        blocked_users = BlockedUsers.query.filter_by(blocker_id=private_user_id).all()

        # Return the list of blocked users
        return jsonify([blocked_user.as_dict() for blocked_user in blocked_users]), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500