from datetime import datetime
import re
from enum import Enum
import uuid
from flask import Response, jsonify
from typing import Dict, List, Optional, Tuple, Any, Union
from app.types.length import USER_PRIVATE_ID_LENGTH

# ----------------- VALIDATE UUID ----------------- #
def valid_uuid(value: Optional[str]) -> bool:
    """
    Validates a UUID based on the Python UUID library.

    Args:
        value (str): The UUID to be validated.

    Returns:
        bool: True if the UUID is valid, False otherwise.
    """
    if value is None:
        return False
    else:
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False

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
            present_fields = [field for field in fields if field in data]
            if len(present_fields) != 1:
                return jsonify({"error": condition["message"]}), 400
        else:
            # Check if at least one of the fields is present
            if not any(field in data for field in fields):
                return jsonify({"error": condition["message"]}), 400

    return jsonify({"message": "Validation passed"}), 200


# ----------------- VALIDATE EMAIL ----------------- #
def valid_email(email: Optional[str]) -> bool:
    """
    Validates an email address based on a simple regex pattern.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if email is None:
        return False
    r = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(r, email) is not None

# ----------------- VALIDATE POST ID ----------------- #
def valid_post_id(value: Optional[str]) -> bool:
    """
    Validates a post identifier based on the UUID format.

    Args:
        value (str): The post identifier to be validated.

    Returns:
        bool: True if the post identifier is valid, False otherwise.
    """
    return valid_uuid(value)
    
# ----------------- VALIDATE ENUM ----------------- #
def valid_enum_element(value: Any, enum_type: type[Enum]) -> bool:
    """
    Validates that a value is a valid enum value.

    Args:
        value (Any): The value to be validated.
        enum_type (type[Enum]): The enum type to validate against.

    Returns:
        bool: True if the value is a valid enum value, False otherwise.
    """
    # Check if value is an instance of the enum type
    if isinstance(value, enum_type):
        value = value.value
    # Ensure value is in the enum's values
    return value in {e.value for e in enum_type}

# ----------------- VALIDATE DATE ----------------- #
def valid_datetime(date: Optional[Any], allow_future_dates=True) -> bool:
    """
    Validates a date to ensure it is not in the future.

    Args:
        date (Any): The date to be validated.
        allow_future_dates (bool): A flag indicating whether future dates are allowed.

    Returns:
        bool: True if the date is valid, False otherwise.
    """
    if not isinstance(date, datetime):
        return False
    if not allow_future_dates and date > datetime.now():
        return False
    return True

# ----------------- VALIDATE INTEGER ----------------- #
def valid_integer(value: Any, allow_negative=False, allow_zero=True) -> bool:
    """
    Validates that a value is an integer.

    Args:
        value (Any): The value to be validated.
        allow_negative (bool): A flag indicating whether negative values are allowed. Defaults to False.
        allow_zero (bool): A flag indicating whether zero is allowed. Defaults to True.

    Returns:
        bool: True if the value is an integer, False otherwise.
    """
    if not isinstance(value, int):
        return False
    if not allow_negative and value < 0:
        return False
    if not allow_zero and value == 0:
        return False
    return True

# ----------------- VALIDATE STRING ----------------- #
def valid_string(value: Any, length: Tuple = (1, 10), allow_empty=False) -> bool:
    """
    Validates that a value is a string within a specified length range.

    Args:
        value (Any): The value to be validated.
        length (Tuple): A tuple containing the minimum and maximum length of the string. Defaults to (1, 10).
        allow_empty (bool): A flag indicating whether an empty string is allowed. Defaults to False.

    Returns:
        bool: True if the value is a string within the specified length range, False otherwise.
    """
    if not isinstance(value, str):
        return False
    if not length[0] <= len(value) <= length[1]:
        return False
    if not allow_empty and len(value) == 0:
        return False
    return True

# ----------------- VALIDATE TEXT ----------------- #
from typing import Any, Tuple

def valid_text(value: Any, length: Tuple[int, int] = (1, 10), limit: bool = False, allow_empty: bool = False) -> bool:
    """
    Validates that a value is a text string within a specified length range.

    Args:
        value (Any): The value to be validated.
        length (Tuple): A tuple containing the minimum and maximum length of the text string. Defaults to (1, 10).
        limit (bool): A flag indicating whether the text string should be strictly limited to the maximum length. Defaults to False.
        allow_empty (bool): A flag indicating whether an empty text string is allowed. Defaults to False.

    Returns:
        bool: True if the value is a valid text string, False otherwise.
    """
    if not isinstance(value, str):
        return False
    
    if allow_empty and len(value) == 0:
        return True

    min_length, max_length = length
    
    if limit and not (min_length <= len(value) <= max_length):
        return False
    
    # If limit is False, check if length meets the minimum length requirement
    if not limit and len(value) < min_length:
        return False
    
    return True


# ----------------- VALIDATE BOOLEAN ----------------- #
def valid_boolean(value: Any) -> bool:  
    """
    Validates that a value is a boolean.

    Args:
        value (Any): The value to be validated.

    Returns:
        bool: True if the value is a boolean, False otherwise.
    """
    return isinstance(value, bool)
