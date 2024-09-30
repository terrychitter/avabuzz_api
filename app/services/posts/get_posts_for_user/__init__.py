from typing import Tuple
from flask import Response, jsonify
from app.models import Users, Posts


def get_posts_for_user(public_user_id: str) -> Tuple[Response, int]:
    """
    Fetches posts from the database for a specific user.

    Args:
        public_user_id (int): The ID of the user to retrieve posts for.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If posts are successfully retrieved, returns a JSON response with the post details and a 200 status code.
            - If the user is not found, returns a JSON response with an error message and a 404 status code.
    """
    try:
        # Check if the user exists in the database
        user = Users.query.filter_by(public_user_id=public_user_id).first()

        if user is None:
            return jsonify({"message": "User not found"}), 404
        
        # Query posts for the specified user
        posts = Posts.query.filter_by(user_id=user.private_user_id).all()

        # Return posts
        return jsonify([post.to_dict(exclude_fields=["user"]) for post in posts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
