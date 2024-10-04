from typing import Tuple
from flask import Response, jsonify
from app.models import Users, UserFollowers

def get_user_following(public_user_id: str) -> Tuple[Response, int]:
    """
    Retrieve the list of users that a user is following.

    Args:
        public_user_id (str): The private user ID of the user whose following list is to be retrieved.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - 200 OK: If the following list is successfully retrieved.
            - 404 Not Found: If the user with the specified public_user_id is not found.
    """
    # Check if the user exists
    user = Users.query.filter_by(public_user_id=public_user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Get the list of users that the user is following
    following = UserFollowers.query.filter_by(follower_user_id=user.private_user_id).all()

    # Return the list of users that the user is following
    return jsonify([followee.to_dict(exclude_fields=["follower"]) for followee in following]), 200
