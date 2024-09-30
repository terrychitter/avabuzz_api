from app import db

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
    __tablename__ = "post_comment_like_counts"

    # COLUMNS
    post_comment_id = db.Column(db.Integer, db.ForeignKey("post_comments.post_comment_id"), primary_key=True)
    post_comment_like_count = db.Column(db.Integer, nullable=False, default=0)

    # Define relationship to PostComments model
    comment = db.relationship("PostComments", back_populates="like_count")

    # METHODS
    def __repr__(self):
        return f"<PostCommentLikeCount {self.post_comment_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostCommentLikeCounts instance into a dictionary representation.

        This method converts the PostCommentLikeCounts instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the PostCommentLikeCounts instance.
        """
        data = {
            "comment": self.comment.to_dict(),
            "like_count": self.post_comment_like_count
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data