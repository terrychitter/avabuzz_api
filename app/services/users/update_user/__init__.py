from typing import Tuple
from flask import Response, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models.users import Users
from app.utils.db_utils import value_exists
from app.utils.validation_utils import valid_email, valid_friend_code

def update_user(private_user_id: str, user_data: dict) -> Tuple[Response, int]:
    """
    Update user information in the database.

    Args:
        private_user_id (str): The private user ID of the user to be updated.
                              This ID is used to find the specific user in the database.
        user_data (dict): A dictionary containing the fields to be updated and their new values.
                          Valid fields include 'username', 'email', 'password', and any other fields
                          present in the `Users` model. The 'password' field will be hashed before
                          updating.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - 200 OK: If the user is successfully updated.
            - 400 Bad Request: If a duplicate username or email is found, or if invalid fields are provided.
            - 404 Not Found: If no user with the specified private_user_id is found.
            - 500 Internal Server Error: If an unexpected error occurs during the process.

    Raises:
        - 400 Bad Request: If the username or email already exists in the database or if invalid fields are provided.
        - 404 Not Found: If the user with the specified private_user_id is not found in the database.
        - 500 Internal Server Error: If an unexpected error occurs, such as a database failure.

    Notes:
        - The 'private_user_id' and 'public_user_id' fields are not modifiable through this function.
        - The 'password' field is hashed using Werkzeug's `generate_password_hash` function before updating.
    """
    try:
        # Fetch the user by private_user_id
        user = Users.query.filter_by(private_user_id=private_user_id).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Check for the presence of the 'password' key and hash it if present
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'])

        invalid_fields = []
        
        # Check for duplicate username or email
        if 'username' in user_data:
            new_username = user_data['username']
            if value_exists(Users, 'username', new_username, {'username': user.username}):
                return jsonify({"message": "Username already exists"}), 400

        if 'email' in user_data:
            # Validate the email format
            if not valid_email(user_data['email']):
                return jsonify({"message": "Invalid email format"}), 400

            new_email = user_data['email']
            if value_exists(Users, 'email', new_email, {'email': user.email}):
                return jsonify({"message": "Email already exists"}), 400
        
        # Validate friend code if present
        # Capitalize the friend code before validation
        user_data['friend_code'] = user_data.get('friend_code', '').upper()
        if 'friend_code' in user_data:
            if not valid_friend_code(user_data['friend_code']):
                return jsonify({"message": "Invalid friend code format"}), 400


        # Update user fields, ensuring that private_user_id and public_user_id are not modified
        for key, value in user_data.items():
            if key in ['private_user_id', 'public_user_id']:
                continue
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                invalid_fields.append(key)

        if invalid_fields:
            return jsonify({"message": "Invalid fields", "invalid_fields": invalid_fields}), 400

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200
    
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
