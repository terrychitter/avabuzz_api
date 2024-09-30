from app import db
from typing import Tuple
from flask import jsonify, Response
from app.models import Users, Posts, UserStats


def delete_post(private_user_id: str, post_id: int) -> Tuple[Response, int]:
    """
    Deletes a post from the database based on the post ID.

    Args:
        private_user_id (str): The private user ID of the user deleting the post.
        post_id (int): The ID of the post to delete.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the post is successfully deleted, returns a JSON response with a success message and a 200 status code.
            - If the post is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during deletion, returns a JSON response with an error message and a 500 status code.
    """
    # Query the post from the database
    post = Posts.query.filter_by(post_id=post_id).first()

    # Check if the post exists
    if post is None:
        # If the post is not found, return a 404 error
        return jsonify({"message": "Post not found"}), 404
    
    # Check if the user is authorized to delete the post
    if post.user_id != private_user_id:
        return jsonify({"message": "Unauthorized to delete this post"}), 403

    try:
        # Decrease the post count for the user
        user = Users.query.filter_by(private_user_id=post.user_id).first()
        if user is not None:
            user_stats = UserStats.query.filter_by(user_id=user.private_user_id).first()
            user_stats.post_count -= 1
            db.session.commit()
        
        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()
        # Return a 200 OK status code with a success message
        return jsonify({"message": "Post deleted"}), 200
    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        # Return a 500 Internal Server Error status code with error details
        return jsonify({"message": "Error deleting post", "error": str(e)}), 500
