from enum import Enum
from app import db
from app.utils.id_generation import generate_uuid

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
    hashtag_id: str = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    hashtag_name: str = db.Column(db.String(50), nullable=False)
    views: int = db.Column(db.Integer, default=0)
    post_count: int = db.Column(db.Integer, default=0)

    # RELATIONSHIPS
    posts = db.relationship("Posts", secondary="post_hashtags", back_populates="hashtags")

    # METHODS
    def __repr__(self):
        return f"<HashTag {self.hashtag_id}>"
    
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