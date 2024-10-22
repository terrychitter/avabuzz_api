from typing import Optional
from app import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import DateTime, Integer, String
from app.utils.id_generation import generate_uuid
from app.models.post.posts import valid_post_id
from app.utils.validation import valid_uuid, valid_datetime, valid_string, valid_integer
from app.types.length import (
    POST_MEDIA_ID_LENGTH,
    POST_ID_LENGTH,
    MEDIA_URL_LENGTH
)

def valid_post_media_id(post_media_id: Optional[str]) -> bool:
    """Validates a post media identifier based on the UUID format.

    Args:
        post_media_id (str): The post media identifier to be validated.

    Returns:
        bool: True if the post media identifier is valid, False otherwise.
    """
    return valid_uuid(post_media_id)


class PostMedia(db.Model): # type: ignore
    """Represents a record of media content for user posts in the database.

    This model stores records of media content for user posts, which can be
    images, videos, or other multimedia files. Each media record is associated
    with a specific post and can have multiple media files.

    Attributes:
        post_media_id (str): The unique identifier for the media record, which serves as the primary key. Defaults to a generated UUID.
        post_id (str): The unique identifier for the post, linked to the `posts` table. This cannot be null.
        media_url (str): The URL of the media file. This cannot be null.
        media_size_bytes (int): The size of the media file in bytes. This cannot be null.
        media_order (int): The order of the media file in the post. This cannot be null.
        created_at (datetime): The timestamp when the media record was created. Defaults to the current time.
    
    Relationships:
        post (Posts): A relationship to the Posts model, indicating the post associated with the media.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_media"

    # COLUMNS
    post_media_id: str = db.Column(String(POST_MEDIA_ID_LENGTH), primary_key=True, default=generate_uuid)
    post_id: str = db.Column(String(POST_ID_LENGTH), db.ForeignKey("posts.post_id"), nullable=False)
    media_url: str = db.Column(String(MEDIA_URL_LENGTH), nullable=False)
    media_size_bytes: int = db.Column(Integer, nullable=False)
    media_order: int = db.Column(Integer, nullable=False)
    created_at: datetime = db.Column(DateTime, nullable=False, default=datetime.now)

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="media")

    #region VALIDATION
    # POST_MEDIA_ID
    @validates("post_media_id")
    def validate_post_media_id(self, key, post_media_id: str) -> str:
        if not valid_post_media_id(post_media_id):
            raise ValueError("Invalid post media ID.")
        return post_media_id
    
    # POST_ID
    @validates("post_id")
    def validate_post_id(self, key, post_id: str) -> str:
        if not valid_post_id(post_id):
            raise ValueError("Invalid post ID.")
        return post_id
    
    # MEDIA_URL
    @validates("media_url")
    def validate_media_url(self, key, media_url: str) -> str:
        if not valid_string(media_url, length=(1, MEDIA_URL_LENGTH), allow_empty=False):
            raise ValueError(f"Invalid media URL length, expected length between 1 and {MEDIA_URL_LENGTH} characters.")
        return media_url
    
    # MEDIA_SIZE_BYTES
    @validates("media_size_bytes")
    def validate_media_size_bytes(self, key, media_size_bytes: int) -> int:
        if not valid_integer(media_size_bytes, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid media size in bytes.")
        return media_size_bytes
    
    # MEDIA_ORDER
    @validates("media_order")
    def validate_media_order(self, key, media_order: int) -> int:
        if not valid_integer(media_order, allow_negative=False, allow_zero=False):
            raise ValueError("Invalid media order.")
        return media_order
    
    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created at datetime.")
        return created_at
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<PostMedia {self.post_media_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostMedia model."""
        ID = "id"
        POST_ID = "post_id"
        URL = "url"
        SIZE_BYTES = "size_bytes"
        ORDER = "order"
        CREATED_AT = "created_at"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the PostMedia instance into a dictionary representation.

        This method converts the PostMedia instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostMedia instance.
        """
        data: dict = {
            "id": self.post_media_id,
            "post_id": self.post_id,
            "url": self.media_url,
            "size_bytes": self.media_size_bytes,
            "order": self.media_order,
            "created_at": self.created_at
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data