from app import db
from typing import Tuple
from flask import Response, jsonify
from app.models import Users, Posts, PostReactions, PostReactionCounts

def unreact_to_post(private_user_id: str, post_id: int) -> Tuple[Response, int]:
    """
    Removes the user's reaction to a post.

    This function performs the following tasks:
    - Checks if the user exists in the database.
    - Checks if the post exists in the database.
    - Checks if the user has already reacted to the post.
    - Updates the reaction count for the post based on the removed reaction.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private user ID of the user unreacting to the post.
        post_id (int): The ID of the post to unreact to.
    
    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the user successfully unreacts to the post, returns a JSON response with a success message and a 200 status code.
            - If the user or post is not found, returns a JSON response with an error message and a 404 status code.
            - If the user has not reacted to the post, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the unreaction process, returns a JSON response with an error message and a 500 status code
    """
    try:
        # Check if the user exists
        user = Users.query.filter_by(private_user_id=private_user_id).first()
        if user is None:
            return jsonify({"message": "User not found"}), 404
        
        # Check if the post exists
        post = Posts.query.filter_by(post_id=post_id).first()
        if post is None:
            return jsonify({"message": "Post not found"}), 404

        # Check if the user has already reacted to the post
        existing_reaction = PostReactions.query.filter_by(post_id=post_id, user_id=private_user_id).first()
        if existing_reaction:
            # Update the reaction count
            reaction_count = PostReactionCounts.query.filter_by(post_id=post_id, post_reaction_type=existing_reaction.post_reaction_type).first()
            reaction_count.reaction_count -= 1

            # Delete the existing reaction
            db.session.delete(existing_reaction)
        else:
            return jsonify({"message": "User has not reacted to post"}), 400

        db.session.commit()
        return jsonify({"message": "Successfully unreacted to post"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error unreacting to post", "error": str(e)}), 500