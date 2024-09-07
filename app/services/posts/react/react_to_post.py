from typing import Tuple
from flask import Response, jsonify
from app import db
from app.models import Users, Posts, PostReactionTypes, PostReactionCounts, PostReactions


def react_to_post(private_user_id: str, post_id: int, reaction: str) -> Tuple[Response, int]:
    """
    Reacts to a post with the specified reaction.

    This function performs the following tasks:
    - Checks if the user exists in the database.
    - Checks if the post exists in the database.
    - Checks if the reaction type is valid.
    - Checks if the user has already reacted to the post.
    - Updates the reaction count for the post based on the new reaction.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private user ID of the user reacting to the post.
        post_id (int): The ID of the post to react to.
        reaction (str): The reaction type to apply to the post.
    
    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the reaction is successfully applied, returns a JSON response with a success message and a 200 status code.
            - If the user or post is not found, returns a JSON response with an error message and a 404 status code.
            - If the reaction type is invalid, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the reaction process, returns a JSON response with an error message and a 500 status code.
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
        
        # Check if the reaction is valid
        post_reaction = PostReactionTypes.query.filter_by(post_reaction_type=reaction).first()
        if post_reaction is None:
            return jsonify({"message": "Invalid reaction type"}), 400

        # Check if the user has already reacted to the post
        existing_reaction = PostReactions.query.filter_by(post_id=post_id, user_id=private_user_id).first()
        if existing_reaction:
            # Decrement the old reaction count
            reaction_count = PostReactionCounts.query.filter_by(post_id=post_id, post_reaction_type=existing_reaction.post_reaction_type).first()
            reaction_count.reaction_count -= 1

            # Delete the existing reaction
            db.session.delete(existing_reaction)

            # Create a new reaction
            new_reaction = PostReactions(
                post_id=post_id,
                user_id=private_user_id,
                post_reaction_type=reaction
            )
            db.session.add(new_reaction)

            # Increment the new reaction count
            new_reaction_count = PostReactionCounts.query.filter_by(post_id=post_id, post_reaction_type=reaction).first()
            new_reaction_count.reaction_count += 1
        else:
            # Create a new reaction
            new_reaction = PostReactions(
                post_id=post_id,
                user_id=private_user_id,
                post_reaction_type=reaction
            )
            db.session.add(new_reaction)

            # Update the reaction count
            reaction_count = PostReactionCounts.query.filter_by(post_id=post_id, post_reaction_type=reaction).first()
            reaction_count.reaction_count += 1   

        db.session.commit()  
        
        return jsonify({"message": f"Reacted to post {post_id} with {reaction}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error reacting to post", "error": str(e)}), 500