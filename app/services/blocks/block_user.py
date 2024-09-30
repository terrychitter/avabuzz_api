from typing import Tuple
from flask import Response, jsonify
from app import db
from app.models.user import Users, BlockedUsers

def block_user(blocker_id: str, blocked_id: str) -> Tuple[Response, int]:
    """
    Block a user.

    This function performs the following tasks:
    - Checks if the blocker exists.
    - Checks if the blocked user exists.
    - Checks if the blocker is trying to block themselves.
    - Checks if the user is already blocked.
    - Blocks the user.

    Args:
        blocker_id (str): The private user ID of the user blocking another user.
        blocked_id (str): The public user ID of the user being blocked.
    """
    try:
        # Check if the blocker exists
        blocker = Users.query.filter_by(private_user_id=blocker_id).first()
        if not blocker:
            return jsonify({"message": "Blocker not found."}), 404
        
        # Check if the blocked user exists
        blocked_user = Users.query.filter_by(public_user_id=blocked_id).first()
        if not blocked_user:
            return jsonify({"message": "Blocked user not found."}), 404
        
        # Check if the blocker is trying to block themselves
        if blocker.private_user_id == blocked_user.private_user_id:
            return jsonify({"message": "User cannot block themselves"}), 400
        
        # Check if the user is already blocked
        blocked = BlockedUsers.query.filter_by(blocker_id=blocker_id, blocked_id=blocked_user.private_user_id).first()
        if blocked:
            return jsonify({"message": "User already blocked"}), 400
        
        # Block the user
        new_blocked_user = BlockedUsers(blocker_id=blocker_id, blocked_id=blocked_user.private_user_id)
        db.session.add(new_blocked_user)

        db.session.commit()
        return jsonify({"message": "User blocked successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500