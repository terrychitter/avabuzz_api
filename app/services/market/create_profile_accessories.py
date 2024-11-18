from app import db
from typing import Any, Dict, Tuple
from flask import Response, jsonify
from datetime import datetime
from app.utils.validation import validate_required_fields
from app.utils.id_generation import generate_uuid
from app.models.market.profile_accessories import ProfileAccessories

def create_profile_accessories(creation_obj: Dict[str, Any]) -> Tuple[Response, int]:
    """
    Create a new market item.

    This function performs the following tasks:
    - Validates the presence of required fields in the creation object.
    - Creates a new market item instance with the provided details.
    - Adds the new market item to the database.
    - Commits the transaction if successful, otherwise rolls back in case of an error.

    If successful, returns a JSON response with a success message.
    If unsuccessful, returns a JSON response with an error message and an appropriate status code.

    Args:
        creation_obj (Dict[str, Any]): A dictionary containing the details of the new market item.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the success or error message.
            - int: HTTP status code (201 for successful creation, 400 for client error).
    """
    try:
        # Create a new market item
        required_fields = [
            {"fields": ["name"], "message": "'name' is required in the creation object."},
            {"fields": ["description"], "message": "'description' is required in the creation object."},
            {"fields": ["url"], "message": "'url' is required in the creation object."},
            {"fields": ["accessory_type"], "message": "'accessory_type' is required in the creation object."},
            {"fields": ["profile_type"], "message": "'profile_type' is required in the creation object."},
            {"fields": ["ownership_type"], "message": "'ownership_type' is required in the creation object."},
            {"fields": ["available"], "message": "'available' is required in the creation object."},
            {"fields": ["bits"], "message": "'bits' is required in the creation object."}
        ]

        # Validate required fields in the creation object
        validation_message, status_code = validate_required_fields(creation_obj, required_fields)
        if status_code != 200:
            return validation_message, status_code
        
        # Create a new market item
        new_market_item = ProfileAccessories(
            accessory_name=creation_obj["name"],
            accessory_description=creation_obj["description"],
            bits=creation_obj["bits"],
            media_url=creation_obj["url"],
            profile_accessory_type=creation_obj["accessory_type"],
            profile_type=creation_obj["profile_type"],
            ownership_type=creation_obj["ownership_type"],
            available=creation_obj["available"],
        )

        # Add the new market item to the database
        db.session.add(new_market_item)
        db.session.commit()

        return jsonify({"message": "Market item created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400