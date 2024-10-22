from typing import Tuple
from flask import Response, jsonify
from app.models import Posts, PostComments


def get_comments_for_post(post_id: int) -> Tuple[Response, int]:
    """
    Fetches comments for a specific post.

    This function performs the following tasks:
    - Retrieves the post from the database.
    - Retrieves the comments associated with the post.
    - Returns a JSON response containing the comments.

    Args:
        post_id (int): The ID of the post to retrieve comments for.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If comments are successfully retrieved, returns a JSON response with the comments and a 200 status code.
            - If the post is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during the retrieval process, returns a JSON response with an error message and a 500 status code.
    """
    try:
        # Check if the post exists
        post = Posts.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Get the comments associated with the post
        comments = PostComments.query.filter_by(post_id=post_id, parent_post_comment_id=None).all()

        return jsonify([comment.to_dict() for comment in comments]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500