from enum import Enum
from app import db
from datetime import datetime
from app.utils.id_generation import generate_uuid

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
    post_comment_like_id: str = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_comment_id: int = db.Column(db.Integer, db.ForeignKey("post_comments.post_comment_id"), nullable=False)
    user_id: str = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Define relationship to PostComments model
    comment = db.relationship("PostComments", back_populates="likes")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="comment_likes")

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