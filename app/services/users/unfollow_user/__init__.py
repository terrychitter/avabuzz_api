from app import db
from typing import Tuple
from flask import Response, jsonify
from app.models import Users, UserFollowers


def unfollow_user(unfollower_private_user_id: str, unfollowee_public_user_id: str) -> Tuple[Response, int]:
    """
    Unfollow a user

    Args:
        unfollower_private_user_id (str): The private_user_id of the user unfollowing the other user
        unfollowee_public_user_id (str): The private_user_id of the user being unfollowed
    
    Returns:
        Tuple[Response, int]: A tuple containing the response and the status code
            - 200 OK: If the user is successfully unfollowed
            - 400 Bad Request: If the unfollower is not following the unfollowee or if the unfollower is trying to unfollow themselves
            - 404 Not Found: If the unfollower or unfollowee is not found
            - 500 Internal Server Error: If an unexpected error occurs while unfollowing the user
    """
    # Check if the unfollower exists in the database
    unfollower = Users.query.filter_by(private_user_id=unfollower_private_user_id).first()
    if not unfollower:
        return jsonify({"message": "Unfollower not found"}), 404
    
    # Check if the unfollowee exists in the database
    unfollowee = Users.query.filter_by(public_user_id=unfollowee_public_user_id).first()
    if not unfollowee:
        return jsonify({"message": "Unfollowee not found"}), 404
    
    # Ensure the unfollower is not trying to unfollow themselves
    if unfollower.private_user_id == unfollowee.private_user_id:
        return jsonify({"message": "Unfollower cannot unfollow themselves"}), 400
    
    # Check if the unfollower is following the unfollowee
    follow = UserFollowers.query.filter_by(follower_user_id=unfollower_private_user_id, followee_user_id=unfollowee.private_user_id).first()
    if not follow:
        return jsonify({"message": "Unfollower is not following this unfollowee"}), 400
    
    # Delete the follow from the database
    try:
        db.session.delete(follow)
        
        # Update the unfollower and unfollowee stats
        unfollower.stats.following_count -= 1
        unfollowee.stats.follower_count -= 1
        
        db.session.commit()
        return jsonify({"message": "User unfollowed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while unfollowing the user", "error": str(e)}), 500