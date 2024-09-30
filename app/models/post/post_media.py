from app import db
from app.utils.id_generation import generate_uuid
import datetime

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
    __tablename__ = "post_media"

    # COLUMNS
    post_media_id = db.Column(db.Integer, primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    media_size_bytes = db.Column(db.Integer, nullable=False)
    media_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="media")

    # METHODS
    def __repr__(self):
        return f"<PostMedia {self.post_media_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostMedia instance into a dictionary representation.

        This method converts the PostMedia instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostMedia instance.
        """
        data = {
            "url": self.media_url,
            "order": self.media_order,
            "size_bytes": self.media_size_bytes,
        }

        for field in exclude_fields:
            data.pop(field, None)

        return data