from flask import Response, jsonify
from typing import Optional, Tuple
from app.models import HashTags

def get_hashtag_posts(hashtag_name: str) -> Tuple[Response, int]:
    """
    Fetches posts associated with a specific hashtag.

    This function performs the following tasks:
    - Retrieves the hashtag with the specified name from the database.
    - Returns a JSON response with 404 status code if the hashtag is not found.
    - Returns a JSON response containing a list of posts associated with the hashtag if found.

    Args:
        hashtag_name (str): The name of the hashtag to retrieve posts for.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing a list of posts associated with the hashtag. 
            - int: HTTP status code (200 for successful retrieval, 404 if the hashtag is not found and 500 for internal server error).
    """
    try:
        # Check if the hashtag exists in the database
        hashtag_name = hashtag_name.lower()
        hashtag = HashTags.query.filter_by(hashtag_name=hashtag_name).first()
        if not hashtag:
            # Return a 404 response if the hashtag is not found
            return jsonify({"error": "Hashtag not found"}), 404
        
        # Return a list of posts associated with the hashtag
        return jsonify([post.to_dict() for post in hashtag.posts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500