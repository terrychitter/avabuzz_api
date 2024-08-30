from typing import Optional, Tuple
from flask import Response
from app.services.posts.get_posts import get_posts
from app.services.posts.create_post import create_post
from app.services.posts.delete_post import delete_post
from app.services.posts.get_posts_for_user import get_posts_for_user

# ----------------- GET POSTS ----------------- #
def get_posts_service(post_id: Optional[int] = None) -> Tuple[Response, int]:
    """
    Fetches posts from the database, either a specific post by ID or all posts.

    This function performs the following tasks:
    - If a `post_id` is provided:
    - Attempts to retrieve the post with the specified ID from the database.
    - Returns a JSON response containing the post details if found.
    - If the post is not found, returns a JSON response with an error message and a 404 status code.
    - If no `post_id` is provided:
    - Retrieves all posts from the database.
    - Returns a JSON response containing a list of all posts.

    Args:
        post_id (Optional[int]): The ID of the post to retrieve. If not provided, all posts are returned.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the post details or a list of all posts. 
            - int: HTTP status code (200 for successful retrieval, 404 if a specific post is not found).

    Raises:
        - 404 Not Found: If a specific post ID is provided but no matching post is found in the database.
    """
    return get_posts(post_id)

# ----------------- CREATE POST ----------------- #
def create_post_service(post_data: dict) -> Tuple[Response, int]:
    """
    Creates a new post in the database based on the provided post data.

    Args:
        post_data (dict): A dictionary containing the data required to create a post. The expected fields are:
            - "post_caption" (str, optional): The caption of the post.
            - "media_urls" (list of dict, optional): A list of dictionaries containing media information. Each dictionary should have:
                - "url" (str): The URL of the media.
                - "size" (int): The size of the media in bytes.
            - "post_type" (str, required): The type of the post, which must match one of the PostType enumeration members.
            - "post_category_id" (int, required): The ID of the post category.
            - "private_user_id" (int, optional): The ID of the user if the post is private to a specific user.
            - "private_group_id" (int, optional): The ID of the group if the post is private to a specific group.
            - "hashtags" (list of str, optional): A list of hashtags associated with the post.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the post is successfully created, returns a JSON response with a success message and a 201 status code.
            - If required fields are missing or invalid, returns a JSON response with an error message and the appropriate status code (400 or 404).
            - If an error occurs during the creation process, returns a JSON response with an error message and a 500 status code.

    Validations:
        - Either 'post_caption' or 'media_urls' must be provided.
        - 'post_type' and 'post_category_id' are required.
        - Either 'private_user_id' or 'private_group_id' must be provided, but not both.

    Process:
        1. Validates required fields using `validate_required_fields`.
        2. Checks if the specified user and category exist in the database.
        3. Validates the post type.
        4. Creates the post and increments the post count for the user.
        5. Adds associated media to the post.
        6. Adds associated hashtags to the post and increments the post count for each hashtag.
        7. Commits the transaction to the database and returns a success message.

    Raises:
        - ValidationError: If required fields are missing or invalid.
        - DatabaseError: If an error occurs during database operations.
    """
    return create_post(post_data)

# ----------------- DELETE POST ----------------- #
def delete_post_service(post_id: int) -> Tuple[Response, int]:
    """
    Deletes a post from the database based on the post ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the post is successfully deleted, returns a JSON response with a success message and a 200 status code.
            - If the post is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during deletion, returns a JSON response with an error message and a 500 status code.
    """
    return delete_post(post_id)

# ----------------- GET POSTS BY USER ----------------- #
def get_posts_for_user_service(private_user_id: int) -> Tuple[Response, int]:
    """
    Fetches all posts associated with a specific user from the database.

    Args:
        private_user_id (int): The ID of the user to retrieve posts for.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing a list of posts associated with the specified user. 
            - int: HTTP status code (200 for successful retrieval, 404 if no user is not found).
    """
    return get_posts_for_user(private_user_id)