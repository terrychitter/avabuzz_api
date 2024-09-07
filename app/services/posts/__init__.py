from typing import Optional, Tuple
from flask import Response
from app.services.posts.get_posts import get_posts
from app.services.posts.create_post import create_post
from app.services.posts.delete_post import delete_post
from app.services.posts.get_posts_for_user import get_posts_for_user
from app.services.posts.react import react_to_post, unreact_to_post
from app.services.posts.comment import get_comments_for_post, comment_on_post, delete_comment, like_comment, unlike_comment

# ----------------- GET POSTS ----------------- #
def get_posts_service(post_id: Optional[int], private_user_id: Optional[str]) -> Tuple[Response, int]:
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
    return get_posts(post_id, private_user_id)

# ----------------- CREATE POST ----------------- #
def create_post_service(private_user_id: str, post_data: dict) -> Tuple[Response, int]:
    """
    Creates a new post in the database based on the provided post data.

    Args:
        private_user_id (str): The private user ID of the user creating the post.
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
    return create_post(private_user_id, post_data)

# ----------------- DELETE POST ----------------- #
def delete_post_service(private_user_id: str, post_id: int) -> Tuple[Response, int]:
    """
    Deletes a post from the database based on the post ID.

    Args:
        private_user_id (str): The private user ID of the user deleting the post.
        post_id (int): The ID of the post to delete.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the post is successfully deleted, returns a JSON response with a success message and a 200 status code.
            - If the post is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during deletion, returns a JSON response with an error message and a 500 status code.
    """
    return delete_post(private_user_id, post_id)

# ----------------- GET POSTS BY USER ----------------- #
def get_posts_for_user_service(public_user_id: str) -> Tuple[Response, int]:
    """
    Fetches posts from the database for a specific user.

    Args:
        public_user_id (str): The ID of the user to retrieve posts for.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If posts are successfully retrieved, returns a JSON response with the post details and a 200 status code.
            - If the user is not found, returns a JSON response with an error message and a 404 status code.
    """
    return get_posts_for_user(public_user_id)

# ----------------- REACT TO POST ----------------- #
def react_to_post_service(private_user_id: str, post_id: int, reaction: str) -> Tuple[Response, int]:
    """
    Reacts to a post with the specified reaction.

    This function performs the following tasks:
    - Checks if the user exists in the database.
    - Checks if the post exists in the database.
    - Checks if the reaction type is valid.
    - Checks if the user has already reacted to the post.
    - Updates the reaction count for the post based on the new reaction.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private user ID of the user reacting to the post.
        post_id (int): The ID of the post to react to.
        reaction (str): The reaction type to apply to the post.
    
    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the reaction is successfully applied, returns a JSON response with a success message and a 200 status code.
            - If the user or post is not found, returns a JSON response with an error message and a 404 status code.
            - If the reaction type is invalid, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the reaction process, returns a JSON response with an error message and a 500 status code.
    """
    return react_to_post(private_user_id, post_id, reaction)

# ----------------- UNREACT TO POST ----------------- #
def unreact_to_post_service(private_user_id: str, post_id: int) -> Tuple[Response, int]:
    """
    Removes the user's reaction to a post.

    This function performs the following tasks:
    - Checks if the user exists in the database.
    - Checks if the post exists in the database.
    - Checks if the user has already reacted to the post.
    - Updates the reaction count for the post based on the removed reaction.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private user ID of the user unreacting to the post.
        post_id (int): The ID of the post to unreact to.
    
    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the user successfully unreacts to the post, returns a JSON response with a success message and a 200 status code.
            - If the user or post is not found, returns a JSON response with an error message and a 404 status code.
            - If the user has not reacted to the post, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the unreaction process, returns a JSON response with an error message and a 500 status code
    """
    return unreact_to_post(private_user_id, post_id)

# ----------------- GET POST COMMENTS ----------------- #
def get_post_comments_service(post_id: int) -> Tuple[Response, int]:
    """
    Fetches comments for a specific post.

    This function performs the following tasks:
    - Retrieves the post from the database.
    - Retrieves the comments associated with the post.
    - Returns a JSON response containing the comments.

    Args:
        post_id (int): The ID of the post to retrieve comments for.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If comments are successfully retrieved, returns a JSON response with the comments and a 200 status code.
            - If the post is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during the retrieval process, returns a JSON response with an error message and a 500 status code.
    """
    return get_comments_for_post(post_id)

# ----------------- COMMENT ON POST ----------------- #
def comment_on_post_service(private_user_id: str, post_id: int, comment_data: dict) -> Tuple[Response, int]:
    """
    Adds a comment to a post.

    This function performs the following tasks:
    - Validates the required fields in the comment data.
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if a parent comment ID is provided.
    - Creates a new comment.
    - Creates a new comment like count entry.

    Args:
        private_user_id (str): The private user ID of the user making the request.
        post_id (int): The ID of the post to comment on.
        comment_data (dict): The comment data.
    
    Returns:
        Tuple[Response, int]: A JSON response and a status code.
            - If successful, the response will contain a message indicating that the comment was added successfully and a status code of 201.
            - If the post, user, or parent comment does not exist, the response will contain an error message and a status code of 404.
            - If an error occurs, the response will contain an error message and a status code of 500.
    """
    return comment_on_post(private_user_id, post_id, comment_data)

# ----------------- DELETE COMMENT ----------------- #
def delete_comment_service(private_user_id: str, post_id: int, comment_id: int) -> Tuple[Response, int]:
    """
    Deletes a comment from a post.

    This function performs the following tasks:
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if the comment exists.
    - Deletes the comment.

    Args:
        private_user_id (str): The private user ID of the user making the request.
        post_id (int): The ID of the post containing the comment.
        comment_id (int): The ID of the comment to delete.

    Returns:
        Tuple[Response, int]: A JSON response and a status code.
            - If successful, the response will contain a message indicating that the comment was deleted successfully and a status code of 200.
            - If the post, user, or comment does not exist, the response will contain an error message and a status code of 404.
            - If an error occurs, the response will contain an error message and a status code of 500.
    """
    return delete_comment(private_user_id, post_id, comment_id)

# ----------------- LIKE COMMENT ----------------- #
def like_comment_service(private_user_id: str, post_id: int, comment_id: int) -> Tuple[Response, int]:
    """
    Likes a comment on a post.

    This function performs the following tasks:
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if the comment exists.
    - Checks if the user has already liked the comment.
    - Creates a new like for the comment.
    - Increments the like count for the comment.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private ID of the user liking the comment.
        post_id (int): The ID of the post containing the comment.
        comment_id (int): The ID of the comment to like.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the comment is successfully liked, returns a JSON response with a success message and a 200 status code.
            - If the user, post, or comment is not found, returns a JSON response with an error message and a 404 status code.
            - If the comment is already liked by the user, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the like process, returns a JSON response with an error message and a 500 status code
    """
    return like_comment(private_user_id, post_id, comment_id)

# ----------------- UNLIKE COMMENT ----------------- #
def unlike_comment_service(private_user_id: str, post_id: int, comment_id: int) -> Tuple[Response, int]:
    """
    Unlikes a comment on a post.

    This function performs the following tasks:
    - Checks if the user exists.
    - Checks if the post exists.
    - Checks if the comment exists.
    - Checks if the user has already liked the comment.
    - Deletes the like for the comment.
    - Decrements the like count for the comment.
    - Commits the changes to the database.

    Args:
        private_user_id (str): The private ID of the user unliking the comment.
        post_id (int): The ID of the post containing the comment.
        comment_id (int): The ID of the comment to unlike.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the comment is successfully unliked, returns a JSON response with a success message and a 200 status code.
            - If the user, post, or comment is not found, returns a JSON response with an error message and a 404 status code.
            - If the comment is not liked by the user, returns a JSON response with an error message and a 400 status code.
            - If an error occurs during the unlike process, returns a JSON response with an error message and a 500 status code
    """
    return unlike_comment(private_user_id, post_id, comment_id)