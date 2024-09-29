import re
from typing import Dict, List, Tuple, Any
from flask import Response, jsonify

# ----------------- VALIDATE REQUIRED FIELDS ----------------- #
def validate_required_fields(data: dict, required_fields: List[Dict[str, Any]]) -> Tuple[Response, int]:
    """
    Validates that the required fields are present based on the provided conditions.
    Supports mutual exclusivity where specified.

    Args:
        data (dict): The dictionary containing the data to be validated.
        required_fields (List[Dict[str, any]]): A list of conditions where each condition is a dictionary with:
            - 'fields': A list of field names where at least one must be present.
            - 'message': The error message to return if none of the fields are present.
            - 'exclusive': Optional boolean indicating that only one of the fields should be present.

    Returns:
        Tuple[Response, int]: A tuple containing a JSON response with the error message and an HTTP status code.
    """
    for condition in required_fields:
        fields = condition["fields"]
        exclusive = condition.get("exclusive", False)

        if exclusive:
            # Check if only one of the exclusive fields is present
            present_fields = [field for field in fields if field in data and data[field]]
            if len(present_fields) != 1:
                return jsonify({"message": condition["message"]}), 400
        else:
            # Check if at least one of the fields is present
            if not any(field in data and data[field] for field in fields):
                return jsonify({"message": condition["message"]}), 400

    return jsonify({"message": "Validation passed"}), 200

# ----------------- VALIDATE EMAIL ----------------- #
def valid_email(email: str) -> bool:
    """
    Validates an email address based on a simple regex pattern.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    return re.fullmatch(regex, email) is not None

# ----------------- VALIDATE FRIEND CODE ----------------- #
def valid_friend_code(friend_code: str) -> bool:
    """
    Validates a friend code based on a simple regex pattern.
    Valid Friend Code Format: **XXX-XXX**, where X is a digit or letter.

    Args:
        friend_code (str): The friend code to be validated.
    
    Returns:
        bool: True if the friend code is valid, False otherwise.
    """
    regex = r'\b[A-Za-z0-9]{2,3}-[A-Za-z0-9]{3}\b'
    
    return re.fullmatch(regex, friend_code) is not None