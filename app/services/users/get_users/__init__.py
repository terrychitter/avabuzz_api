from flask import jsonify, Response
from typing import Optional, Tuple
from app.models.users import Users

def get_users(public_user_id: Optional[str] = None) -> Tuple[Response, int]:
    """
    Retrieve user information from the database.

    Args:
        public_user_id (Optional[str]): The public user ID to filter users by.
                                         If provided, the function returns the user with this ID.
                                         If not provided, the function returns all users.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If `public_user_id` is provided and a matching user is found, returns the user data as JSON
              and a 200 status code.
            - If `public_user_id` is provided but no matching user is found, returns a JSON response with
              an error message and a 404 status code.
            - If `public_user_id` is not provided, returns a list of all users as JSON and a 200 status code.

    Raises:
        - 404 Not Found: If a specific user ID is provided but the user is not found.
        - 200 OK: When a user or list of users is successfully retrieved from the database.
    """
    if public_user_id:
        # Query the user from the database using the public_user_id
        user = Users.query.filter_by(public_user_id=public_user_id).first()

        # If the user is not found, return a 404 error
        if user is None:
            return jsonify({"message": "User not found"}), 404

        # Return the user as JSON
        return jsonify(user.to_dict()), 200
    else:
        # Query all the users from the database
        users = Users.query.all()

        # Convert the users to a list of dictionaries
        users_list = [user.to_dict() for user in users]

        # Return the list of users as JSON
        return jsonify(users_list), 200
