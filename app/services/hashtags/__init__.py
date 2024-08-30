from typing import Optional, Tuple
from flask import Response
from app.services.hashtags.get_hashtags import get_hashtags
from app.services.hashtags.get_hashtag_posts import get_hashtag_posts

# ----------------- GET HASHTAGS ----------------- #
def get_hashtags_service(hashtag_name: Optional[str] = None) -> Tuple[Response, int]:
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
    return get_hashtags(hashtag_name)

# ----------------- GET POSTS FOR HASHTAG ----------------- #
def get_posts_for_hashtag_service(hashtag_name: str) -> Tuple[Response, int]:
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
    return get_hashtag_posts(hashtag_name)