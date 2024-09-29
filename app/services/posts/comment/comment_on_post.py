from app import db
from typing import Tuple
from flask import Response, jsonify
from app.models import Users, Posts, PostComments, PostCommentLikeCounts
from app.utils.validation_utils import validate_required_fields


def comment_on_post(private_user_id: str, post_id: int, comment_data: dict) -> Tuple[Response, int]:
    """
    Adds a comment to a post.

    This function performs the following tasks:
    - Validates the required fields in the comment data.
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if a parent comment ID is provided.
    - Creates a new comment.
    - Creates a new comment like count entry.

    Args:
        private_user_id (str): The private user ID of the user making the request.
        post_id (int): The ID of the post to comment on.
        comment_data (dict): The comment data.
    
    Returns:
        Tuple[Response, int]: A JSON response and a status code.
            - If successful, the response will contain a message indicating that the comment was added successfully and a status code of 201.
            - If the post, user, or parent comment does not exist, the response will contain an error message and a status code of 404.
            - If an error occurs, the response will contain an error message and a status code of 500.
    """
    try:
        # Validate required fields in the comment data
        required_fields = [   
            {"fields": ["content"], "message": "'content' is required in the comment data."}
        ]

        validation_message, status_code = validate_required_fields(comment_data, required_fields)
        if status_code != 200:
            return validation_message, status_code
        
        # Check if the user exists
        user = Users.query.get(private_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if the post exists
        post = Posts.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Check if a parent comment ID is provided
        parent_post_comment_id = comment_data.get("parent_post_comment_id")
        if parent_post_comment_id:
            # Check if the parent comment exists
            parent_comment = PostComments.query.get(parent_post_comment_id)
            if not parent_comment:
                return jsonify({"error": "Parent comment not found"}), 404
        
        # Create a new comment
        new_comment = PostComments(
            post_comment_text=comment_data["content"],
            post_id=post_id,
            user_id=private_user_id,
            parent_post_comment_id=parent_post_comment_id
        )
        db.session.add(new_comment)
        db.session.commit()

        # Create a new comment like count entry
        new_comment_like_count = PostCommentLikeCounts(post_comment_id=new_comment.post_comment_id, post_comment_like_count=0)
        db.session.add(new_comment_like_count)
        db.session.commit()

        return jsonify({"message": "Comment added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500