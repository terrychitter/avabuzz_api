from flask import Response, jsonify
from typing import Optional, Tuple
from app.models import HashTags

def get_hashtags(hashtag_name: Optional[str] = None) -> Tuple[Response, int]:
    """
    Fetches hashtags from the database, either a specific hashtag by ID or all hashtags.

    This function performs the following tasks:
    - If a `hashtag_name` is provided:
        - Attempts to retrieve the hashtag with the specified name from the database.
        - Returns a JSON reponse with 404 status code if the hashtag is not found.
        - Returns a JSON response containing the hashtag details if found.
    - If no `hashtag_name` is provided:
        - Retrieves all hashtags from the database.
        - Returns a JSON response containing a list of all hashtags.

    Args:
        hashtag_name (Optional[str]): The hashtag name of the hashtag to retrieve. If not provided, all hashtags are returned.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the hashtag details or a list of all hashtags. 
            - int: HTTP status code (200 for successful retrieval, 404 if a specific hashtag is not found and 500 for internal server error).
    """
    try:
        # Check if a specific hashtag name is provided
        if hashtag_name:
            # Check if the hashtag exists in the database
            hashtag_name = hashtag_name.lower()
            hashtag = HashTags.query.filter_by(hashtag_name=hashtag_name).first()
            if hashtag:
                # Return the hashtag
                return jsonify({"hashtag": hashtag.to_dict()}), 200
            else:
                # Return a 404 response if the hashtag is not found
                return jsonify({"error": "Hashtag not found"}), 404
        else:
            # Fetch all hashtags from the database
            hashtags = HashTags.query.all()
            # Return a list of all hashtags
            return jsonify({"hashtags": [hashtag.to_dict() for hashtag in hashtags]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500