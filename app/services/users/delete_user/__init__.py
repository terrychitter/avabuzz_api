from app import db
from flask import jsonify
from typing import Tuple
from flask import Response
from app.models import Users


def delete_user(public_user_id: str) -> Tuple[Response, int] :
    """
    Deletes a user from the database based on the user ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the user is successfully deleted, returns a JSON response with a success message and a 200 status code.
            - If the user is not found, returns a JSON response with an error message and a 404 status code.
    """
    # Query the user from the database
    user = Users.query.filter_by(public_user_id=public_user_id).first()

    if user is None:
        # If the user is not found, return a 404 error
        return jsonify({"message": "User not found"}), 404

    try:
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()
        # Return a 200 OK status code with a success message
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        # Return a 500 Internal Server Error status code with error details
        return jsonify({"message": "Error deleting user", "error": str(e)}), 500