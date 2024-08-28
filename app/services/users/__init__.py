from flask import Response
from typing import Optional, Tuple
from app.services.users.create_user import create_user
from app.services.users.get_users import get_users
from app.services.users.delete_user import delete_user
from app.services.users.update_user import update_user


# ----------------- CREATE USER ----------------- #
def create_user_service(user_data: dict) -> Tuple[Response, int]:
    """
    Creates a new user with the provided details.

    This function performs the following tasks:
    - Extracts user data from the JSON request body.
    - Validates the presence of required fields (`username`, `email`, and `password`).
    - Checks for the existence of a user with the same email or username in the database.
    - Generates unique public and private IDs for the new user.
    - Creates a new user instance with the hashed password and associates it with the generated IDs.
    - Adds the new user and ID records to the database.
    - Commits the transaction if successful, otherwise rolls back in case of an error.

    If successful, returns a JSON response with a success message and the details of the created user.
    If unsuccessful, returns a JSON response with an error message and an appropriate status code.

    Returns:
        Tuple[Response, int]: 
            - Response: JSON response containing the success or error message.
            - int: HTTP status code (201 for successful creation, 400 for client error, 500 for server error).

    Raises:
        - 400 Bad Request: If required fields are missing or if the email or username already exists.
        - 500 Internal Server Error: If an error occurs during database operations.
    """
    return create_user(user_data)

# ----------------- GET USERS ----------------- #
def get_users_service(public_user_id: Optional[str]=None) -> Tuple[Response, int]:
    """
    Retrieve user information from the database.

    Args:
        public_user_id (Optional[str]): The public user ID to filter users by.
                                         If provided, the function returns the user with this ID.
                                         If not provided, the function returns all users.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If `public_user_id` is provided and a matching user is found, returns the user data as JSON
              and a 200 status code.
            - If `public_user_id` is provided but no matching user is found, returns a JSON response with
              an error message and a 404 status code.
            - If `public_user_id` is not provided, returns a list of all users as JSON and a 200 status code.

    Raises:
        - 404 Not Found: If a specific user ID is provided but the user is not found.
        - 200 OK: When a user or list of users is successfully retrieved from the database.
    """
    return get_users(public_user_id)

# ----------------- UPDATE THE USER ----------------- #
def update_user_service(public_user_id: str, user_data: dict) -> Tuple[Response, int]:
    """
    Update user information in the database.

    Args:
        public_user_id (str): The public user ID of the user to be updated.
                              This ID is used to find the specific user in the database.
        user_data (dict): A dictionary containing the fields to be updated and their new values.
                          Valid fields include 'username', 'email', 'password', and any other fields
                          present in the `Users` model. The 'password' field will be hashed before
                          updating.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - 200 OK: If the user is successfully updated.
            - 400 Bad Request: If a duplicate username or email is found, or if invalid fields are provided.
            - 404 Not Found: If no user with the specified public_user_id is found.
            - 500 Internal Server Error: If an unexpected error occurs during the process.

    Raises:
        - 400 Bad Request: If the username or email already exists in the database or if invalid fields are provided.
        - 404 Not Found: If the user with the specified public_user_id is not found in the database.
        - 500 Internal Server Error: If an unexpected error occurs, such as a database failure.

    Notes:
        - The 'public_user_id' and 'private_user_id' fields are not modifiable through this function.
        - The 'password' field is hashed using Werkzeug's `generate_password_hash` function before updating.
    """
    return update_user(public_user_id, user_data)

# ----------------- DELETE USER ----------------- #
def delete_user_service(public_user_id: str) -> Tuple[Response, int]:
    """
    Deletes a user from the database based on the user ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the user is successfully deleted, returns a 204 status code.
            - If the user is not found, returns a JSON response with an error message and a 404 status code.
    """
    return delete_user(public_user_id)