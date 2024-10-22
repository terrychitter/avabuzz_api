from app import db
from sqlalchemy import String
from sqlalchemy.orm import validates
from app.utils.validation import valid_string
from enum import Enum
from app.types.length import (
    POST_REACTION_TYPE_LENGTH
)

def valid_post_reaction_type(post_reaction_type: str) -> bool:
    """Validates a post reaction type.

    Args:
        post_reaction_type (str): The post reaction type to be validated.

    Returns:
        bool: True if the post reaction type is valid, False otherwise.
    """
    return valid_string(post_reaction_type, length=(1, POST_REACTION_TYPE_LENGTH), allow_empty=False)

class PostReactionTypes(db.Model): # type: ignore
    """Represents a record of reaction types for user posts in the database.

    This model stores the different types of reactions that users can have on
    posts, such as likes, dislikes, etc. Each reaction type is associated with
    a specific post and user.

    Attributes:
        post_reaction_type (str): The unique identifier for the reaction type, which serves as the primary key.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_reaction_types"

    # COLUMNS
    post_reaction_type: str = db.Column(String(POST_REACTION_TYPE_LENGTH), primary_key=True)

    #region VALIDATION
    # POST_REACTION_TYPE
    @validates("post_reaction_type")
    def validate_post_reaction_type(self, key, post_reaction_type: str) -> str:
        if not valid_post_reaction_type(post_reaction_type):
            raise ValueError("Invalid post reaction type.")
        return post_reaction_type
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<PostReactionType {self.post_reaction_type.upper()}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostReactionTypes model."""
        TYPE = "type"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """
        Converts the PostReactionTypes instance into a dictionary representation.

        This method converts the PostReactionTypes instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostReactionTypes instance.
        """
        data: dict = {
            "type": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data