from typing import Dict, List, Tuple
from flask import Response, jsonify


def validate_required_fields(post_data: dict, conditions: List[Dict[str, any]]) -> Tuple[Response, int]:
    """
    Validates that the required fields are present based on the provided conditions.
    Supports mutual exclusivity where specified.

    Args:
        post_data (dict): The dictionary containing the data to be validated.
        conditions (List[Dict[str, any]]): A list of conditions where each condition is a dictionary with:
            - 'fields': A list of field names where at least one must be present.
            - 'message': The error message to return if none of the fields are present.
            - 'exclusive': Optional boolean indicating that only one of the fields should be present.

    Returns:
        Tuple[Response, int]: A tuple containing a JSON response with the error message and an HTTP status code.
    """
    for condition in conditions:
        fields = condition["fields"]
        exclusive = condition.get("exclusive", False)

        if exclusive:
            # Check if only one of the exclusive fields is present
            present_fields = [field for field in fields if field in post_data and post_data[field]]
            if len(present_fields) != 1:
                return jsonify({"message": condition["message"]}), 400
        else:
            # Check if at least one of the fields is present
            if not any(field in post_data and post_data[field] for field in fields):
                return jsonify({"message": condition["message"]}), 400

    return None, None