from typing import Optional, Union
from app import db
from enum import Enum
from datetime import datetime
from app.types.enum import CommentStatus
from app.utils.id_generation import generate_uuid
from app.models.user.users import valid_user_id
from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, String, Text
from sqlalchemy.orm import validates
from app.utils.validation import valid_uuid, valid_post_id, valid_enum_element, valid_datetime, valid_text
from app.types.length import (
    POST_COMMENT_ID_LENGTH,
    POST_ID_LENGTH,
    USER_PRIVATE_ID_LENGTH,
    PARENT_POST_COMMENT_ID_LENGTH
)

def valid_post_comment_id(post_comment_id: Optional[str]) -> bool:
    """Validates a post comment identifier based on the UUID format.

    Args:
        post_comment_id (str): The post comment identifier to be validated.

    Returns:
        bool: True if the post comment identifier is valid, False otherwise.
    """
    return valid_uuid(post_comment_id)

class PostComments(db.Model): # type: ignore
    """
    Represents a record of comments on user posts in the database.

    This model stores records of comments on user posts, which can be parent
    comments or replies to existing comments. Each comment is associated with
    a specific post and user, and can have multiple likes.

    Attributes:
        post_comment_id (str): The unique identifier for the post comment, which serves as the primary key. Defaults to a generated UUID.
        post_id (str): The unique identifier for the post, linked to the `posts` table. This cannot be null.
        user_id (str): The unique identifier for the user who created the comment, linked to the `users` table. This cannot be null.
        post_comment_text (str): The text content of the comment. This cannot be null.
        post_comment_status (CommentStatus): The status of the comment, which is an enumeration of comment statuses. Defaults to NORMAL.
        parent_post_comment_id (int, optional): The unique identifier for the parent comment, if the comment is a reply. This can be null.
        created_at (datetime): The timestamp when the comment was created. Defaults to the current time.
    
    Relationships:
        post (Posts): A relationship to the Posts model, indicating the post associated with the comment.
        user (Users): A relationship to the Users model, indicating the user who created the comment.
        parent_comment (PostComments): A self-referential relationship to the PostComments model, indicating the parent comment for replies.
        replies (PostComments): A relationship to the PostComments model, indicating the replies to the comment.
        likes (PostCommentLikes): A relationship to the PostCommentLikes model, indicating the likes on the comment.
        like_count (PostCommentLikeCounts): A relationship to the PostCommentLikeCounts model, indicating the like count on the comment.
    """
    # TABLE NAME
    __tablename__: str = "post_comments"

    # COLUMNS
    post_comment_id: str = db.Column(String(POST_COMMENT_ID_LENGTH), primary_key=True, default=generate_uuid)
    post_id: str = db.Column(String(POST_ID_LENGTH), db.ForeignKey("posts.post_id"), nullable=False)
    user_id: str = db.Column(String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=False)
    post_comment_text: str = db.Column(Text, nullable=False)
    post_comment_status: CommentStatus = db.Column(SQLAlchemyEnum(CommentStatus), nullable=False, default=CommentStatus.NORMAL)
    parent_post_comment_id: str = db.Column(String(PARENT_POST_COMMENT_ID_LENGTH), db.ForeignKey("post_comments.post_comment_id"), nullable=True)
    created_at: datetime = db.Column(DateTime, nullable=False, default=datetime.now)

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="comments")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="comments")

    # Define self-referential relationship for parent comments and replies
    parent_comment = db.relationship("PostComments", backref=db.backref("replies", cascade="all, delete-orphan"), remote_side=[post_comment_id])

    # Define relationship to PostCommentLikes model
    likes = db.relationship("PostCommentLikes", back_populates="comment", cascade="all, delete-orphan")

    # Define relationship to PostCommentLikeCounts model
    like_count = db.relationship("PostCommentLikeCounts", back_populates="comment", cascade="all, delete-orphan")

    #region VALIDATION
    # POST_COMMENT_ID
    @validates("post_comment_id")
    def validate_post_comment_id(self, key, post_comment_id: str) -> str:
        if not valid_post_comment_id(post_comment_id):
            raise ValueError("Invalid post comment ID")
        return post_comment_id
    
    # POST_ID
    @validates("post_id")
    def validate_post_id(self, key, post_id: str) -> str:
        if not valid_post_id(post_id):
            raise ValueError("Invalid post ID")
        return post_id
    
    # USER_ID
    @validates("user_id")
    def validate_user_id(self, key, user_id: str) -> str:
        if not valid_user_id(user_id):
            raise ValueError("Invalid user ID")
        return user_id
    
    # POST_COMMENT_TEXT
    @validates("post_comment_text")
    def validate_post_comment_text(self, key, post_comment_text: str) -> str:
        if valid_text(post_comment_text, limit=False, allow_empty=False):
            raise ValueError("Invalid post comment text")
        return post_comment_text
    
    # POST_COMMENT_STATUS
    @validates("post_comment_status")
    def validate_post_comment_status(self, key, post_comment_status: Union[CommentStatus, str]) -> str:
        if not valid_enum_element(post_comment_status, CommentStatus):
            raise ValueError("Invalid comment status")
        return CommentStatus(post_comment_status).value
    
    # PARENT_POST_COMMENT_ID
    @validates("parent_post_comment_id")
    def validate_parent_post_comment_id(self, key, parent_post_comment_id: str) -> str:
        if not valid_post_comment_id(parent_post_comment_id):
            raise ValueError("Invalid parent post comment ID")
        return parent_post_comment_id

    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created at datetime")
        return created_at
    #endregion

    # METHODS
    def __repr__(self):
        return f"<PostComment {self.post_comment_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostComments model."""
        ID = "id"
        POST_ID = "post_id"
        USER = "user"
        CONTENT = "content"
        STATUS = "status"
        LIKE_COUNT = "like_count"
        CREATED_AT = "created_at"
        REPLIES = "replies"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the PostComments instance into a dictionary representation.

        This method converts the PostComments instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostComments instance.
        """
        like_count_relationship = getattr(self, "like_count", [])
        
        data: dict = {
            "id": self.post_comment_id,
            "post_id": self.post_id,
            "user": self.user.to_dict(),
            "content": self.post_comment_text,
            "status": self.post_comment_status.value,
            "like_count": like_count_relationship[0].post_comment_like_count if like_count_relationship and len(like_count_relationship) > 0 else 0,
            "created_at": self.created_at,
            "replies": [reply.to_dict() for reply in self.replies] if self.replies else []
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data