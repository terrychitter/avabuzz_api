from app import db
from typing import Tuple
from flask import Response, jsonify
from app.models import Users, Posts, PostComments


def delete_comment(private_user_id: str, post_id: int, comment_id: int) -> Tuple[Response, int]:
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
        
        # Check if the user is the author of the comment
        if comment.user_id != private_user_id:
            return jsonify({"error": "You are not authorized to delete this comment"}), 403
        
        # Delete the comment
        db.session.delete(comment)

        db.session.commit()
        return jsonify({"message": "Comment deleted successfully"}), 200     
    except Exception as e:
        return jsonify({"error": str(e)}), 500