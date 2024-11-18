import datetime
from typing import Tuple, List
from app import db
from flask import Response, jsonify, request
from app.utils.id_generation import generate_uuid
from werkzeug.security import generate_password_hash
from app.utils.id_generation import generate_unique_public_id
from app.models import (Users,
                        UserStats,
                        UserPublicId,
                        ProfileAccessories,
                        UserProfileAccessories,
                        OwnedAccessories)

def add_initial_owned_accessories(user_id: str, accessories: List[ProfileAccessories]) -> None:
    for accessory in accessories:
        owned_accessory = OwnedAccessories(
            user_id=user_id,
            accessory_id=accessory.accessory_id,
        )
        db.session.add(owned_accessory)

def create_user(user_data: dict) -> Tuple[Response, int]:
    """
    Creates a new user with the provided details.

    This function performs the following tasks:
    - Extracts user data from the input dictionary.
    - Validates the presence of required fields (`username`, `email`, and `password`).
    - Checks for the existence of a user with the same email or username in the database.
    - Generates unique public and private IDs for the new user.
    - Creates instances to store the generated IDs.
    - Creates a new user instance with the hashed password and associates it with the generated IDs.
    - Adds the new user and ID records to the database.
    - Adds default accessories to the user's owned accessories and sets them as active.
    - Commits the transaction if successful, otherwise rolls back in case of an error.

    If successful, returns a JSON response with a success message and the details of the created user.
    If unsuccessful, returns a JSON response with an error message and an appropriate status code.

    Args:
        user_data (dict): A dictionary containing the user details (`username`, `email`, `password`).

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the success or error message.
            - int: HTTP status code (201 for successful creation, 400 for client error, 500 for server error).

    Raises:
        - 400 Bad Request: If required fields are missing or if the email or username already exists.
        - 500 Internal Server Error: If an error occurs during database operations.
    """
    try:
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

        # Create instances for storing public and private IDs
        user_public_id = UserPublicId(public_id=public_id)

        # Create a new user instance with the provided data
        new_user = Users(
            private_user_id=generate_uuid(),
            public_user_id=public_id,
            username=user_data["username"],
            email=user_data["email"],
            password_hash=generate_password_hash(user_data["password"]),
        )

        # Add user stats
        user_stats = UserStats(user_id=new_user.private_user_id, follower_count=0, following_count=0, post_count=0)

        # Add the new user and ID records to the database and commit the transaction
        db.session.add(new_user)
        db.session.add(user_stats)
        db.session.add(user_public_id)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # Return a success response with the created user details
    return jsonify({"message": "User created successfully", "user": new_user.to_dict()}), 201


