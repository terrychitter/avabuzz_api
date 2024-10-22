from app import db
from enum import Enum
from sqlalchemy.orm import validates
from app.utils.validation import valid_integer
from app.models.post.posts import valid_post_id
from app.models.post.post_reaction_types import valid_post_reaction_type
from sqlalchemy import Integer, String
from app.types.length import (
    POST_ID_LENGTH,
    POST_REACTION_TYPE_LENGTH
)

class PostReactionCounts(db.Model): # type: ignore
    """Represents a record of reaction counts on user posts in the database.

    This model stores the total number of reactions on user posts, which is used
    to display the reaction count on the post. Each reaction count is associated
    with a specific post and reaction type.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        post_reaction_type (str): The type of reaction, linked to the `post_reaction_types` table. This serves as part of the primary key.
        reaction_count (int): The total number of reactions of the specified type on the post. Defaults to 0.

    Relationships:
        post (Posts): A relationship to the Posts model, indicating the post associated with the reaction count.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_reaction_counts"

    # COLUMNS
    post_id: str = db.Column(String(POST_ID_LENGTH), db.ForeignKey("posts.post_id"), primary_key=True)
    post_reaction_type: str = db.Column(String(POST_REACTION_TYPE_LENGTH), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)
    reaction_count: int = db.Column(Integer, nullable=False, default=0)

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="reactions")

    #region VALIDATION
    # POST_ID
    @validates("post_id")
    def validate_post_id(self, key, post_id: str) -> str:
        if not valid_post_id(post_id):
            raise ValueError("Invalid post ID.")     
        return post_id

    # POST_REACTION_TYPE
    @validates("post_reaction_type")
    def validate_post_reaction_type(self, key, post_reaction_type: str) -> str:
        if not valid_post_reaction_type(post_reaction_type):
            raise ValueError("Invalid post reaction type.")
        return post_reaction_type
    
    # REACTION_COUNT
    @validates("reaction_count")
    def validate_reaction_count(self, key, reaction_count: int) -> int:
        if not valid_integer(reaction_count, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid reaction count.")
        return reaction_count
    #endregion VALIDATION
    
    # METHODS
    def __repr__(self):
        return f"<PostReactionCount {self.post_id} {self.post_reaction_type.upper()}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostReactionCounts model."""
        POST_ID = "post_id"
        REACTION_TYPE = "reaction_type"
        REACTION_COUNT = "reaction_count"

    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the PostReactionCounts instance into a dictionary representation.

        This method converts the PostReactionCounts instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the PostReactionCounts instance.
        """
        data: dict = {
            "post_id": self.post_id,
            "type": self.post_reaction_type,
            "count": self.reaction_count
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data