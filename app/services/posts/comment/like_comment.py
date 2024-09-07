from typing import Tuple
from flask import Response, jsonify
from app import db
from app.models import Users, Posts, PostComments, PostCommentLikes, PostCommentLikeCounts


def like_comment(private_user_id: str, post_id: int, comment_id: int) -> Tuple[Response, int]:
    """
    Likes a comment on a post.

    This function performs the following tasks:
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if the comment exists.
    - Checks if the user has already liked the comment.
    - Creates a new like for the comment.
    - Increments the like count for the comment.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private ID of the user liking the comment.
        post_id (int): The ID of the post containing the comment.
        comment_id (int): The ID of the comment to like.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the comment is successfully liked, returns a JSON response with a success message and a 200 status code.
            - If the user, post, or comment is not found, returns a JSON response with an error message and a 404 status code.
            - If the comment is already liked by the user, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the like process, returns a JSON response with an error message and a 500 status code
    """
    try:
        # Check if the user exists
        user = Users.query.get(private_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if the post exists
        post = Posts.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Check if the comment exists
        comment = PostComments.query.get(comment_id)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Check if the user has already liked the comment
        existing_like = PostCommentLikes.query.filter_by(user_id=private_user_id, post_comment_id=comment_id).first()
        if existing_like:
            return jsonify({"error": "Comment already liked"}), 400
        
        # Create a new like for the comment
        new_like = PostCommentLikes(user_id=private_user_id, post_comment_id=comment_id)

        # Add the like to the database session
        db.session.add(new_like)

        # Increment the like count for the comment
        like_count = PostCommentLikeCounts.query.filter_by(post_comment_id=comment_id).first()
        like_count.post_comment_like_count += 1

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Comment liked successfully"}), 200     
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500