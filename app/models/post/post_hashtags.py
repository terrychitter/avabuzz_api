from app import db

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
    __tablename__ = "post_hashtags"

    # COLUMNS
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), primary_key=True)
    hashtag_id = db.Column(db.String(36), db.ForeignKey("hashtags.hashtag_id"), primary_key=True)

    # Define relationship to HashTags model
    hashtag = db.relationship("HashTags", backref="post_hashtag")

    # METHODS
    def __repr__(self):
        return f"<PostHashTag {self.post_id}-{self.hashtag_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostHashTags instance into a dictionary representation.

        This method converts the PostHashTags instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostHashTags instance.
        """
        data = {
            "post_id": self.post_id,
            "hashtag_id": self.hashtag_id
        }

        for field in exclude_fields:
            data.pop(field, None)

        return data