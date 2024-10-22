from typing import Optional
import uuid
from app import db
from enum import Enum
from sqlalchemy import String, Text
from sqlalchemy.orm import validates
from app.utils.id_generation import generate_uuid
from app.utils.validation import valid_uuid, valid_string
from app.types.length import (
    POST_CATEGORY_ID_LENGTH,
    POST_CATEGORY_NAME_LENGTH_MIN,
    POST_CATEGORY_NAME_LENGTH_MAX
)

def valid_post_category_id(post_category_id: Optional[str]) -> bool:
    """Validates a post category identifier based on the UUID format.

    Args:
        post_category_id (str): The post category identifier to be validated.

    Returns:
        bool: True if the post category identifier is valid, False otherwise.
    """
    return valid_uuid(post_category_id)

class PostCategories(db.Model): # type: ignore
    """Represents a record of post categories in the database.

    This model stores records of post categories, which are used to categorize
    and group user posts by topic. Each post category can have multiple posts.

    Attributes:
        post_category_id (str): The unique identifier for the post category, which serves as the primary key. Defaults to a generated UUID.
        post_category_name (str): The name of the post category. This cannot be null.
        post_category_description (str, optional): The description of the post category. This can be null.
    
    Relationships:
        posts (Posts): A relationship to the Posts model, indicating the posts associated with the category.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_categories"

    # COLUMNS
    post_category_id: str = db.Column(String(POST_CATEGORY_ID_LENGTH), primary_key=True, default=generate_uuid)
    post_category_name: str = db.Column(String(POST_CATEGORY_NAME_LENGTH_MAX), nullable=False)
    post_category_description: str = db.Column(Text, nullable=True)

    # Define the relationship to the Posts model
    posts = db.relationship("Posts", back_populates="post_category")

    #region VALIDATION
    # POST_CATEGORY_ID
    @validates("post_category_id")
    def validate_post_category_id(self, key, post_category_id: str) -> str:
        if not valid_post_category_id(post_category_id):
            raise ValueError("Invalid post category identifier.")
        return post_category_id
    
    # POST_CATEGORY_NAME
    @validates("post_category_name")
    def validate_post_category_name(self, key, post_category_name: str) -> str:
        if not valid_string(post_category_name, length=(POST_CATEGORY_NAME_LENGTH_MIN, POST_CATEGORY_NAME_LENGTH_MAX), allow_empty=False):
            raise ValueError(f"Invalid post category name length, expected length between {POST_CATEGORY_NAME_LENGTH_MIN} and {POST_CATEGORY_NAME_LENGTH_MAX} characters.")
        return post_category_name
    #endregion
    
    # METHODS
    def __repr__(self):
        return f"<PostCategory {self.post_category_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostCategories model."""
        ID = "id"
        NAME = "name"
        DESCRIPTION = "description"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """
        Converts the PostCategories instance into a dictionary representation.

        This method converts the PostCategories instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostCategories instance.
        """
        data: dict = {
            "id": self.post_category_id,
            "name": self.post_category_name,
            "description": self.post_category_description
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data