from app import db
from typing import Tuple
from flask import Response, jsonify
from app.models import Users, BlockedUsers

def unblock_user(unblocker_id: str, unblocked_id: str) -> Tuple[Response, int]:
    try:
        # Check if the unblocker exists
        unblocker = Users.query.filter_by(private_user_id=unblocker_id).first()
        if not unblocker:
            return jsonify({"message": "Unblocker not found."}), 404
        
        # Check if the unblocked user exists
        unblocked_user = Users.query.filter_by(public_user_id=unblocked_id).first()
        if not unblocked_user:
            return jsonify({"message": "Blocked user not found."}), 404
        
        # Check if the unblocker is trying to unblock themselves
        if unblocker.private_user_id == unblocked_user.private_user_id:
            return jsonify({"message": "User cannot unblock themselves"}), 400
        
        # Check if the user is already unblocked
        blocked = BlockedUsers.query.filter_by(blocker_id=unblocker_id, blocked_id=unblocked_user.private_user_id).first()
        if not blocked:
            return jsonify({"message": "User not blocked"}), 400
        
        # Unblock the user
        db.session.delete(blocked)

        db.session.commit()
        return jsonify({"message": "User unblocked"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500