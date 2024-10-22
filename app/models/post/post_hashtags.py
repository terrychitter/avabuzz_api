from app import db
from enum import Enum
from sqlalchemy import String
from sqlalchemy.orm import validates
from app.utils.validation import valid_uuid
from app.models.post.posts import valid_post_id
from app.models.post.hashtags import valid_hashtag_id
from app.types.length import (
    POST_ID_LENGTH,
    HASHTAG_ID_LENGTH
)

class PostHashTags(db.Model): # type: ignore
    """Represents a record of hashtags associated with user posts in the database.

    This model stores records of hashtags associated with user posts, which are
    used to categorize and group posts by topic. Each hashtag is associated with
    a specific post and can have multiple posts.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        hashtag_id (str): The unique identifier for the hashtag, linked to the `hashtags` table. This serves as part of the primary key.
    
    Relationships:
        hashtag (HashTags): A relationship to the HashTags model, indicating the hashtag associated with the post.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_hashtags"

    # COLUMNS
    post_id: str = db.Column(String(POST_ID_LENGTH), db.ForeignKey("posts.post_id"), primary_key=True)
    hashtag_id: str = db.Column(String(HASHTAG_ID_LENGTH), db.ForeignKey("hashtags.hashtag_id"), primary_key=True)

    # Define relationship to HashTags model
    hashtag = db.relationship("HashTags", backref="post_hashtag")

    #region VALIDATION
    # POST_ID
    @validates("post_id")
    def validate_post_id(self, key, post_id: str) -> str:
        if not valid_post_id(post_id):
            raise ValueError("Invalid post ID.")
        return post_id
    
    # HASHTAG_ID
    @validates("hashtag_id")
    def validate_hashtag_id(self, key, hashtag_id: str) -> str:
        if not valid_hashtag_id(hashtag_id):
            raise ValueError("Invalid hashtag ID.")
        return hashtag_id
    #endregion

    # METHODS
    def __repr__(self):
        return f"<PostHashTag {self.post_id}-{self.hashtag_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostHashTags model."""
        POST_ID = "post_id"
        HASHTAG_ID = "hashtag_id"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []):
        """Converts the PostHashTags instance into a dictionary representation.

        This method converts the PostHashTags instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostHashTags instance.
        """
        data: dict = {
            "post_id": self.post_id,
            "hashtag": self.hashtag.to_dict()
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data