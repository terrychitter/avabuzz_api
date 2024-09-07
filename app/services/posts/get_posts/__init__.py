from typing import Optional, Tuple
from flask import Response, jsonify
from app.models.posts import Posts

def get_posts(post_id: Optional[int], private_user_id: Optional[str]) -> Tuple[Response, int]:
    """
    Fetches posts from the database, either a specific post by ID or all posts.

    This function performs the following tasks:
    - If a `post_id` is provided:
    - Attempts to retrieve the post with the specified ID from the database.
    - Returns a JSON response containing the post details if found.
    - If the post is not found, returns a JSON response with an error message and a 404 status code.
    - If no `post_id` is provided:
    - Retrieves all posts from the database.
    - Returns a JSON response containing a list of all posts.

    Args:
        post_id (Optional[int]): The ID of the post to retrieve. If not provided, all posts are returned.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the post details or a list of all posts. 
            - int: HTTP status code (200 for successful retrieval, 404 if a specific post is not found).

    Raises:
        - 404 Not Found: If a specific post ID is provided but no matching post is found in the database.
    """
    # Get post by ID if post_id is provided
    if post_id:
        post = Posts.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        return jsonify(post.to_dict(user_id=private_user_id if private_user_id else None)), 200
    
    # Get all posts if post_id is not provided
    posts = Posts.query.all()
    return jsonify([post.to_dict(user_id=private_user_id if private_user_id else None) for post in posts]), 200