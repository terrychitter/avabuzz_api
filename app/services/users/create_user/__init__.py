from typing import Tuple
from app import db
from flask import Response, jsonify, request
from app.models.users import Users
from app.models.user_public_ids import UserPublicId
from app.models.user_private_ids import UserPrivateId
from werkzeug.security import generate_password_hash
from app.utils.id_generation import generate_unique_public_id, generate_unique_private_id

def create_user(user_data: dict) -> Tuple[Response, int]:
    """
    Creates a new user with the provided details.

    This function performs the following tasks:
    - Extracts user data from the JSON request body.
    - Validates the presence of required fields (`username`, `email`, and `password`).
    - Checks for the existence of a user with the same email or username in the database.
    - Generates unique public and private IDs for the new user.
    - Creates a new user instance with the hashed password and associates it with the generated IDs.
    - Adds the new user and ID records to the database.
    - Commits the transaction if successful, otherwise rolls back in case of an error.

    If successful, returns a JSON response with a success message and the details of the created user.
    If unsuccessful, returns a JSON response with an error message and an appropriate status code.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the success or error message.
            - int: HTTP status code (201 for successful creation, 400 for client error, 500 for server error).

    Raises:
        - 400 Bad Request: If required fields are missing or if the email or username already exists.
        - 500 Internal Server Error: If an error occurs during database operations.
    """
    # Define required fields for user creation
    required_fields = ["username", "email", "password"]

    # Validate that all required fields are present
    for field in required_fields:
        if field not in user_data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    # Check if a user with the same email already exists
    existing_user = Users.query.filter_by(email=user_data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    # Check if a user with the same username already exists
    existing_user = Users.query.filter_by(username=user_data["username"]).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    
    # Generate unique IDs for the new user
    public_id = generate_unique_public_id(db.session)
    private_id = generate_unique_private_id(db.session)

    # Create instances for storing public and private IDs
    user_public_id = UserPublicId(public_id=public_id)
    user_private_id = UserPrivateId(private_id=private_id)

    # Create a new user instance with the provided data
    new_user = Users(
        public_user_id=public_id,
        private_user_id=private_id,
        username=user_data["username"],
        email=user_data["email"],
        password_hash=generate_password_hash(user_data["password"]),
    )

    try:
        # Add the new user and ID records to the database and commit the transaction
        db.session.add(new_user)
        db.session.add(user_public_id)
        db.session.add(user_private_id)
        db.session.commit()
    except Exception as e:
        # Rollback the transaction in case of an error and return an error message
        db.session.rollback()
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

    # Return a success response with the created user details
    return (
        jsonify({"message": "User created successfully", "user": new_user.as_dict()}),
        201,
    )
