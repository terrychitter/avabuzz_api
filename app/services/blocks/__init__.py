from typing import Tuple
from flask import Response
from app.services.blocks.get_blocked_users import get_blocked_users
from app.services.blocks.block_user import block_user
from app.services.blocks.unblock_user import unblock_user


# ----------------- GET BLOCKED USERS ----------------- #
def get_blocked_users_service(private_user_id: str) -> Tuple[Response, int]:
    """
    Get the list of users blocked by the user.

    This function performs the following tasks:
    - Checks if the user exists.
    - Retrieves the list of blocked users.
    - Returns the list of blocked users.

    Args:
        private_user_id (str): The private user ID of the user.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - If the user is found, returns a JSON response with the list of blocked users and a 200 status code.
            - If the user is not found, returns a JSON response with an error message and a 404 status code.
            - If an error occurs during the process, returns a JSON response with an error message and a 500 status code.
    """
    return get_blocked_users(private_user_id)

# ----------------- BLOCK USER ----------------- #
def block_user_service(blocker_id: str, blocked_id: str) -> Tuple[Response, int]:
    """
    Block a user.

    This function performs the following tasks:
    - Checks if the blocker exists.
    - Checks if the blocked user exists.
    - Checks if the blocker is trying to block themselves.
    - Checks if the user is already blocked.
    - Blocks the user.

    Args:
        blocker_id (str): The private user ID of the user blocking another user.
        blocked_id (str): The public user ID of the user being blocked.
    """
    return block_user(blocker_id, blocked_id)

# ----------------- UNBLOCK USER ----------------- #
def unblock_user_service(unblocker_id: str, unblocked_id: str) -> Tuple[Response, int]:
    return unblock_user(unblocker_id, unblocked_id)