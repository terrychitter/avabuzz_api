from typing import Tuple
from flask import Response, jsonify
from app.models import Users, UserFollowers
from app.utils.io import PAGE, PER_PAGE, paginate_query

def get_user_followers(public_user_id: str, page: int = PAGE, per_page: int = PER_PAGE) -> Tuple[Response, int]:
    """
    Retrieve the list of followers for a user.

    Args:
        public_user_id (str): The public user ID of the user whose followers are to be retrieved.

    Returns:
        Tuple[Response, int]: A tuple containing the Flask response object and an HTTP status code.
            - 200 OK: If the followers are successfully retrieved.
            - 404 Not Found: If the user with the specified public_user_id is not found.
    """
    try:
        # Check if the user exists
        user = Users.query.filter_by(public_user_id=public_user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get the list of followers
        followers = UserFollowers.query.filter_by(followee_user_id=user.private_user_id)

        # Paginate the list of followers
        data = paginate_query(
            query=followers,
            per_page=per_page,
            page=page,
            items_name="followers",
            to_representation=lambda follower: follower.to_dict(exclude_fields=[UserFollowers.DictKeys.FOLLOWEE])
        )

        # Return the list of followers
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500