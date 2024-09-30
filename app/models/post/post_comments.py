from app import db
from enum import Enum
from app.utils.id_generation import generate_uuid
from sqlalchemy import Enum as SQLAlchemyEnum

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
    __tablename__ = "post_comments"

    class CommentStatus(Enum):
        """Enumeration of comment statuses for the PostComments model.

        This enumeration defines the different statuses that a comment can have,
        including normal comments, hidden comments, and flagged comments.

        Attributes:
            NORMAL (str): A normal comment that is visible to users.
            HIDDEN (str): A hidden comment that is not visible to users.
            FLAGGED (str): A flagged comment that requires moderation.
        
        Returns:
            None
        """
        NORMAL = "NORMAL"
        HIDDEN = "HIDDEN"
        FLAGGED = "FLAGGED"

    # COLUMNS
    post_comment_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    post_comment_text = db.Column(db.Text, nullable=False)
    post_comment_status = db.Column(SQLAlchemyEnum(CommentStatus), nullable=False, default=CommentStatus.NORMAL)
    parent_post_comment_id = db.Column(db.Integer, db.ForeignKey("post_comments.post_comment_id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

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

    # METHODS
    def __repr__(self):
        return f"<PostComment {self.post_comment_id}>"
    
    def to_dict(self, exclude_fields: list = ["post"]):
        """Converts the PostComments instance into a dictionary representation.

        This method converts the PostComments instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostComments instance.
        """
        like_count_relationship = getattr(self, "like_count", [])
        
        data = {
            "id": self.post_comment_id,
            "post": self.post.to_dict(),
            "user": self.user.to_dict(),
            "content": self.post_comment_text,
            "status": self.post_comment_status.value,
            "like_count": like_count_relationship[0].post_comment_like_count if like_count_relationship and len(like_count_relationship) > 0 else 0,
            "created_at": self.created_at,
            "replies": [reply.to_dict() for reply in self.replies] if "replies" not in exclude_fields else []
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data