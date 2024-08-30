from typing import Tuple
from flask import Response, jsonify
from app.models import Users, UserFollowers

def get_user_followers(private_user_id: str) -> Tuple[Response, int]:
    """
    Retrieve the list of followers for a user.

    Args:
        private_user_id (str): The public user ID of the user whose followers are to be retrieved.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - 200 OK: If the followers are successfully retrieved.
            - 404 Not Found: If the user with the specified private_user_id is not found.
    """
    # Check if the user exists
    user = Users.query.filter_by(private_user_id=private_user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Get the list of followers
    followers = UserFollowers.query.filter_by(followee_user_id=user.private_user_id).all()

    # Return the list of followers
    return jsonify([follower.to_dict(exclude_fields=["followee"]) for follower in followers]), 200