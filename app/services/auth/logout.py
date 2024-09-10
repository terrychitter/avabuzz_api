from app import db
from typing import Tuple
from flask import Response, jsonify
from app.models import JWTTokenBlocklist


def logout(jti: str) -> Tuple[Response, int]:
    """
    Logs out a user.

    This function adds the user's JWT token to the blocklist.

    Args:
        jti (str): The JWT ID of the token to be added to the blocklist.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the logout is successful, returns a JSON response with a message and a 200 status code.
            - If an error occurs during the logout process, returns a JSON response with an error message and a 500 status code
    """
    try:
        # Add the JTI to the blocklist
        token = JWTTokenBlocklist(jti=jti)
        db.session.add(token)
        db.session.commit()

        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500