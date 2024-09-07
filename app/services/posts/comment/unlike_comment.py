from typing import Tuple
from flask import Response, jsonify
from app import db
from app.models import Users, Posts, PostComments, PostCommentLikes, PostCommentLikeCounts


def unlike_comment(private_user_id: str, post_id: int, comment_id) -> Tuple[Response, int]:
    """
    Unlikes a comment on a post.

    This function performs the following tasks:
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if the comment exists.
    - Checks if the user has liked the comment.
    - Deletes the like for the comment.
    - Decrements the like count for the comment.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private ID of the user unliking the comment.
        post_id (int): The ID of the post containing the comment.
        comment_id (int): The ID of the comment to unlike.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the comment is successfully unliked, returns a JSON response with a success message and a 200 status code.
            - If the user, post, or comment is not found, returns a JSON response with an error message and a 404 status code.
            - If the comment is not liked by the user, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the unlike process, returns a JSON response with an error message and a 500 status code
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
        
        # Check if the user has liked the comment
        existing_like = PostCommentLikes.query.filter_by(user_id=private_user_id, post_comment_id=comment_id).first()
        if not existing_like:
            return jsonify({"error": "Comment not liked"}), 400
        
        # Delete the like for the comment
        db.session.delete(existing_like)

        # Decrement the like count for the comment
        like_count = PostCommentLikeCounts.query.filter_by(post_comment_id=comment_id).first()
        like_count.post_comment_like_count -= 1

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Comment unliked"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500