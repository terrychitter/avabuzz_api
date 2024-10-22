from app import db
from enum import Enum
from sqlalchemy import String
from sqlalchemy.orm import validates
from app.models.post.posts import valid_post_id
from app.models.post.post_reaction_types import valid_post_reaction_type
from app.models.user.users import valid_user_id
from app.types.length import (
    POST_ID_LENGTH,
    USER_PRIVATE_ID_LENGTH,
    POST_REACTION_TYPE_LENGTH
)

class PostReactions(db.Model): # type: ignore
    """
    Represents a record of reactions on user posts in the database.
    
    This model stores records of reactions on user posts, indicating the users
    who reacted to a specific post. Each reaction is associated with a specific
    post and user, and can be of different types such as likes, dislikes, etc.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        user_id (str): The unique identifier for the user who reacted to the post, linked to the `users` table. This serves as part of the primary key.
        post_reaction_type (str): The type of reaction, linked to the `post_reaction_types` table. This serves as part of the primary key.

    Relationships:
        user (Users): A relationship to the Users model, indicating the user who reacted to the post.
        post (Posts): A relationship to the Posts model, indicating the post associated with the reaction.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_reactions"

    # COLUMNS
    post_id: str = db.Column(String(POST_ID_LENGTH), db.ForeignKey("posts.post_id"), primary_key=True)
    user_id: str = db.Column(String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), primary_key=True)
    post_reaction_type: str = db.Column(String(POST_REACTION_TYPE_LENGTH), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="post_reactions")

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="post_reactions")

    #region VALIDATION
    # POST_ID
    @validates("post_id")
    def validate_post_id(self, key, post_id: str) -> str:
        if not valid_post_id(post_id):
            raise ValueError("Invalid post ID.")
        return post_id
    
    # USER_ID
    @validates("user_id")
    def validate_user_id(self, key, user_id: str) -> str:
        if not valid_user_id(user_id):
            raise ValueError("Invalid user ID.")
        return user_id
    
    # POST_REACTION_TYPE
    @validates("post_reaction_type")
    def validate_post_reaction_type(self, key, post_reaction_type: str) -> str:
        if not valid_post_reaction_type(post_reaction_type):
            raise ValueError("Invalid post reaction type.")
        return post_reaction_type
    #endregion VALIDATION
    
    # METHODS
    def __repr__(self):
        return f"<PostReaction {self.post_id} {self.user_id} {self.post_reaction_type.upper()}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostReactions model."""
        POST_ID = "post_id"
        USER_ID = "user_id"
        REACTION = "reaction"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []):
        """Converts the PostReactions instance into a dictionary representation.

        This method converts the PostReactions instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostReactions instance.
        """
        data: dict = {
            "post_id": self.post_id,
            "user": self.user.to_dict(),
            "reaction": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data