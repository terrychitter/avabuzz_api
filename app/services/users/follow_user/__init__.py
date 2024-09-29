from typing import Tuple
from flask import Response, jsonify
from app.models import Users, UserFollowers, UserStats
from app import db


def follow_user(follower_private_user_id: str, followee_public_user_id: str) -> Tuple[Response, int]:
    """
    Follow a user

    Args:
        follower_private_user_id (str): The private_user_id of the user following the other user
        followee_public_user_id (str): The private_user_id of the user being followed

    Returns:
        Tuple[Response, int]: A tuple containing the response and the status code
            - 200 OK: If the user is successfully followed
            - 400 Bad Request: If the follower is already following the followee or if the follower is trying to follow themselves
            - 404 Not Found: If the follower or followee is not found
            - 500 Internal Server Error: If an unexpected error occurs while following the user
    """
    # Check if the follower exists in the database
    follower = Users.query.filter_by(private_user_id=follower_private_user_id).first()
    if not follower:
        return jsonify({"message": "Follower not found"}), 404
    
    # Check if the followee exists in the database
    followee = Users.query.filter_by(public_user_id=followee_public_user_id).first()
    if not followee:
        return jsonify({"message": "Followee not found"}), 404
    
    # Ensure the follower is not following themselves
    if follower.private_user_id == followee.private_user_id:
        return jsonify({"message": "Follower cannot follow themselves"}), 400
    
    # Check if the follower is already following the followee
    if UserFollowers.query.filter_by(follower_user_id=follower.private_user_id, followee_user_id=followee.private_user_id).first():
        return jsonify({"message": "Follower is already following this followee"}), 400
    
    # Create a new UserFollowers object
    new_follow = UserFollowers(follower_user_id=follower.private_user_id, followee_user_id=followee.private_user_id)

    # Add the new follow to the database
    try:
        db.session.add(new_follow)

        # Update the follower and followee stats
        follower.stats.following_count += 1
        followee.stats.follower_count += 1

        db.session.commit()
        return jsonify({"message": "User followed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while following the user", "error": str(e)}), 500
    

    
