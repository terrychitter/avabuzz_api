from typing import Optional
import uuid
from app import db
from enum import Enum
from sqlalchemy.orm import validates
from sqlalchemy import Integer, String
from app.utils.id_generation import generate_uuid
from app.utils.validation import valid_uuid, valid_string, valid_integer
from app.types.length import (
    HASHTAG_ID_LENGTH,
    HASHTAG_NAME_LENGTH_MIN,
    HASHTAG_NAME_LENGTH_MAX
)

def valid_hashtag_id(hashtag_id: Optional[str]) -> bool:
    """Validates a hashtag identifier.

    Args:
        hashtag_id (str): The hashtag identifier to be validated.

    Returns:
        bool: True if the hashtag identifier is valid, False otherwise.
    """
    return valid_uuid(hashtag_id)

def valid_hashtag_name(hashtag_name: Optional[str]) -> bool:
    """Validates a hashtag name.

    Args:
        hashtag_name (str): The hashtag name to be validated.

    Returns:
        bool: True if the hashtag name is valid, False otherwise.
    """
    return valid_string(hashtag_name, length=(HASHTAG_NAME_LENGTH_MIN, HASHTAG_NAME_LENGTH_MAX), allow_empty=False)

def valid_hashtag_views(views: int) -> bool:
    """Validates the views count for a hashtag.

    Args:
        views (int): The views count to be validated.

    Returns:
        bool: True if the views count is valid, False otherwise.
    """
    return valid_integer(views, allow_negative=False, allow_zero=True)

def valid_hashtag_post_count(post_count: int) -> bool:
    """Validates the post count for a hashtag.

    Args:
        post_count (int): The post count to be validated.

    Returns:
        bool: True if the post count is valid, False otherwise.
    """
    return valid_integer(post_count, allow_negative=False, allow_zero=True)

class HashTags(db.Model): # type: ignore
    """Represents a record of hashtags used within posts in the system.

    This model tracks hashtags that users can assign to posts, along with 
    metadata about each hashtag such as its name, view count, and the number 
    of posts associated with it.

    Attributes:
        hashtag_id (str): The unique identifier for the hashtag record. Defaults to a UUID.
        hashtag_name (str): The name of the hashtag, which cannot be null.
        views (int): The total number of views the hashtag has received. Defaults to `0`.
        post_count (int): The number of posts that have been tagged with this hashtag. Defaults to `0`.

    Relationships:
        posts (Posts): A many-to-many relationship with posts, indicating which posts 
                       are associated with this hashtag.

    Methods:
        to_dict(exclude_fields=[]): Converts the HashTags instance into a dictionary 
            representation, allowing for exclusion of specified fields.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "hashtags"

    # COLUMNS
    hashtag_id: str = db.Column(String(HASHTAG_ID_LENGTH), primary_key=True, default=generate_uuid)
    hashtag_name: str = db.Column(String(HASHTAG_NAME_LENGTH_MAX), nullable=False)
    views: int = db.Column(Integer, default=0)
    post_count: int = db.Column(Integer, default=0)

    # RELATIONSHIPS
    posts = db.relationship("Posts", secondary="post_hashtags", back_populates="hashtags")

    #region VALIDATION
    @validates("hashtag_id")
    def validate_hashtag_id(self, key, hashtag_id: str) -> str:
        if not valid_hashtag_id(hashtag_id):
            raise ValueError("Invalid hashtag identifier.")
        return hashtag_id
    
    @validates("hashtag_name")
    def validate_hashtag_name(self, key, hashtag_name: str) -> str:
        if not valid_hashtag_name(hashtag_name):
            raise ValueError(f"Inavlid hashtag name")
        return hashtag_name
    
    @validates("views")
    def validate_views(self, key, views: int) -> int:
        if not valid_hashtag_views(views):
            raise ValueError("Invalid views count.")
        return views
    
    @validates("post_count")
    def validate_post_count(self, key, post_count: int) -> int:
        if not valid_hashtag_post_count(post_count):
            raise ValueError("Invalid post count.")
        return post_count
    #endregion

    # METHODS
    def __repr__(self):
        return f"<HASHTAG ID {self.hashtag_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the HashTags model."""
        ID = "id"
        NAME = "name"
        VIEWS = "views"
        POST_COUNT = "post_count"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the HashTags instance into a dictionary representation.

        This method converts the HashTags instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the HashTags instance.
        """
        data: dict = {
            "id": self.hashtag_id,
            "name": self.hashtag_name,
            "views": self.views,
            "post_count": self.post_count
        }
    
        for field in exclude_fields:
            data.pop(field.value, None)
    
        return data