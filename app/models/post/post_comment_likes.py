from typing import Optional
import uuid
from app import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import DateTime, String
from app.utils.id_generation import generate_uuid
from app.models.post.post_comments import valid_post_comment_id
from app.models.user.users import valid_private_user_id
from app.utils.validation import valid_datetime, valid_uuid
from app.types.length import (
    POST_COMMENT_LIKE_ID_LENGTH,
    POST_COMMENT_ID_LENGTH,
    USER_PRIVATE_ID_LENGTH
)

def valid_post_comment_like_id(post_comment_like_id: Optional[str]) -> bool:
    """Validates a post comment like identifier based on the UUID format.

    Args:
        post_comment_like_id (str): The post comment like identifier to be validated.

    Returns:
        bool: True if the post comment like identifier is valid, False otherwise.
    """
    return valid_uuid(post_comment_like_id)

class PostCommentLikes(db.Model): # type: ignore
    """Represents a record of likes on post comments in the database.

    This model stores records of likes on post comments, indicating the users
    who liked a specific comment. Each like is associated with a post comment
    and a user who liked the comment.

    Attributes:
        post_comment_like_id (str): The unique identifier for the post comment like, which serves as the primary key. Defaults to a generated UUID.
        post_comment_id (int): The unique identifier for the post comment, linked to the `post_comments` table. This cannot be null.
        user_id (str): The unique identifier for the user who liked the comment, linked to the `users` table. This cannot be null.
        created_at (datetime): The timestamp when the like was created. Defaults to the current time.

    Relationships:
        comment (PostComments): A relationship to the PostComments model, indicating the comment associated with the like.
        user (Users): A relationship to the Users model, indicating the user who liked the comment.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "post_comment_likes"

    # COLUMNS
    post_comment_like_id: str = db.Column(String(POST_COMMENT_LIKE_ID_LENGTH), primary_key=True, default=generate_uuid)
    post_comment_id: str = db.Column(String(POST_COMMENT_LIKE_ID_LENGTH), db.ForeignKey("post_comments.post_comment_id"), nullable=False)
    user_id: str = db.Column(String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=False)
    created_at: datetime = db.Column(DateTime, nullable=False, default=datetime.now)

    # Define relationship to PostComments model
    comment = db.relationship("PostComments", back_populates="likes")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="comment_likes")

    #region VALIDATION
    # POST_COMMENT_LIKE_ID
    @validates("post_comment_like_id")
    def validate_post_comment_like_id(self, key, post_comment_like_id: str) -> str:
        if not valid_post_comment_like_id(post_comment_like_id):
            raise ValueError("Invalid post comment like identifier.")
        return post_comment_like_id
    
    # POST_COMMENT_ID
    @validates("post_comment_id")
    def validate_post_comment_id(self, key, post_comment_id: str) -> str:
        if not valid_post_comment_id(post_comment_id):
            raise ValueError("Invalid post comment ID.")
        return post_comment_id
    
    # USER_ID
    @validates("user_id")
    def validate_user_id(self, key, user_id: str) -> str:
        if not valid_private_user_id(user_id):
            raise ValueError("Invalid user ID.")
        return user_id
    
    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created at timestamp.")
        return created_at
    #endregion

    # METHODS
    def __repr__(self):
        return f"<PostCommentLike {self.post_comment_like_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostCommentLikes model."""
        ID = "id"
        COMMENT_ID = "comment_id"
        USER = "user"
        CREATED_AT = "created_at"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the PostCommentLikes instance into a dictionary representation.

        This method converts the PostCommentLikes instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostCommentLikes instance.
        """
        data: dict = {
            "id": self.post_comment_like_id,
            "comment_id": self.post_comment_id,
            "user": self.user.to_dict(),
            "created_at": self.created_at
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data