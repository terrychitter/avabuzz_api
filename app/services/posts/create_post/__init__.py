from app import db
from typing import Tuple
from app.models.users import Users, UserStats
from flask import jsonify, Response
from app.models import PostCategories, PostMedia, Posts, PostHashTags, PostReactionCounts, PostReactionTypes
from app.models.hashtags import HashTags
from app.utils.validation_utils import validate_required_fields

def create_post(post_data: dict) -> Tuple[Response, int]:
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

    try:
        # Define the required field conditions for a new post
        required_conditions = [
            {"fields": ["post_caption", "media_urls"], "message": "Either 'post_caption' or 'media_urls' is required."},
            {"fields": ["post_type"], "message": "'post_type' is required."},
            {"fields": ["post_category_id"], "message": "'post_category_id' is required."},
            {"fields": ["private_user_id", "private_group_id"], "message": "Either 'private_user_id' or 'private_group_id' is required.", "exclusive": True}
        ]
        
        # Validate required fields using the reusable method
        validation_error, status_code = validate_required_fields(post_data, required_conditions)
        if validation_error:
            return validation_error, status_code
        
        # If user_id is provided, check if the user exists
        if "private_user_id" in post_data:
            user = Users.query.filter_by(private_user_id=post_data["private_user_id"]).first()
            if not user:
                return jsonify({"message": "User not found"}), 404
            
        # If group_id is provided, check if the group exists
        # TODO: Add group validation here

        # Check if the category exists
        category = PostCategories.query.get(post_data["post_category_id"])
        if not category:
            return jsonify({"message": "Category not found"}), 404
        
        # Check if the post type is valid
        if post_data["post_type"] not in Posts.PostType.__members__:
            return jsonify({"message": "Invalid post type"}), 400
        
        # Create the post
        new_post = Posts(
            post_caption=post_data.get("post_caption"),
            post_type=Posts.PostType[post_data["post_type"]],
            post_category_id=post_data["post_category_id"],
            user_id=post_data.get("private_user_id"),
        )

        # Increment the post count for the user
        user_stats = UserStats.query.filter_by(user_id=post_data["private_user_id"]).first()
        user_stats.post_count += 1

        # Save the post to the database first
        db.session.add(new_post)

        # Get unique post reaction types
        reaction_types = PostReactionTypes.query.all()

        # Create post reaction counts for each reaction type
        for reaction_type in reaction_types:
            post_reaction_count = PostReactionCounts(post_id=new_post.post_id, post_reaction_type=reaction_type.post_reaction_type)
            db.session.add(post_reaction_count)

        # Commit the initial post and reaction counts to the database
        db.session.commit()
        
        # Add the media to the post
        for index, media_data in enumerate(post_data["media_urls"]):
            media_url = media_data["url"]
            media_size = media_data["size"]
            media = PostMedia(
                post_id=new_post.post_id,
                media_url=media_url,
                media_size_bytes=media_size,
                media_order=index
            )
            db.session.add(media)

        # Add the hashtags to the post
        if "hashtags" in post_data:
            for hashtag in post_data["hashtags"]:
                hashtag = hashtag.lower()
                # Check if the hashtag exists
                hashtag_obj = HashTags.query.filter_by(hashtag_name=hashtag).first()
                if not hashtag_obj:
                    hashtag_obj = HashTags(hashtag_name=hashtag)
                    db.session.add(hashtag_obj)
                    db.session.commit()
                
                # Add the hashtag to the post
                post_hashtag = PostHashTags(post_id=new_post.post_id, hashtag_id=hashtag_obj.hashtag_id)
                db.session.add(post_hashtag)

                # Increment the post count for the hashtag
                hashtag_obj.post_count += 1
                db.session.commit()
        
        # Commit all changes to the database after adding media and hashtags
        db.session.commit()

        return jsonify({"message": "Post created successfully", "post": new_post.to_dict()}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({"message": "An error occurred while creating the post", "error": str(e)}), 500




