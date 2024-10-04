from app import db
from enum import Enum

class PostCommentLikeCounts(db.Model): # type: ignore
    """Represents a record of like counts for post comments in the database.

    This model stores the total number of likes on a post comment, which is used
    to display the like count on the comment. Each comment can have multiple likes.

    Attributes:
        post_comment_id (int): The unique identifier for the post comment, linked to the `post_comments` table. This serves as the primary key.
        post_comment_like_count (int): The total number of likes on the post comment. Defaults to 0.
    
    Relationships:
        comment (PostComments): A relationship to the PostComments model, indicating the comment associated with the like count.
    """
    # TABLE NAME
    __tablename__: str = "post_comment_like_counts"

    # COLUMNS
    post_comment_id: str = db.Column(db.String(36), db.ForeignKey("post_comments.post_comment_id"), primary_key=True)
    post_comment_like_count: int = db.Column(db.Integer, nullable=False, default=0)

    # Define relationship to PostComments model
    comment = db.relationship("PostComments", back_populates="like_count")

    # METHODS
    def __repr__(self):
        return f"<PostCommentLikeCount {self.post_comment_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the PostCommentLikeCounts model."""
        COMMENT_ID = "comment_id"
        LIKE_COUNT = "like_count"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the PostCommentLikeCounts instance into a dictionary representation.

        This method converts the PostCommentLikeCounts instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the PostCommentLikeCounts instance.
        """
        data: dict = {
            "comment_id": self.post_comment_id,
            "like_count": self.post_comment_like_count
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data