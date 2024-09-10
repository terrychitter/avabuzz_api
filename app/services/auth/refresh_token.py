import datetime
from typing import Tuple
from flask import Response, jsonify
from flask_jwt_extended import create_access_token


def refresh_token(identity: str) -> Tuple[Response, int]:
    """
    Refreshes the user's access token.

    This function generates a new access token for the user.

    Args:
        identity (str): The user's private user ID.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the refresh is successful, returns a JSON response with a new access token and a 200 status code.
            - If an error occurs during the refresh process, returns a JSON response with an error message and a 500 status code
    """
    try:
        access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(minutes=15))
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500