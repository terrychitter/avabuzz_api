from app import db

class UserStats(db.Model): # type: ignore
    """Represents the statistics of a user account.

    This model stores statistical information about a user, including the number of followers,
    following, and posts made by the user.

    Attributes:
        user_id (str): The unique identifier for the user, serving as the primary key.
        follower_count (int): The number of followers for the user, which cannot be null.
        following_count (int): The number of users that the user is following, which cannot be null.
        post_count (int): The number of posts created by the user, which cannot be null.
    
    Relationships:
        user (Users): A relationship to the Users model, indicating the user associated with the statistics.
    """
    # TABLE NAME
    __tablename__ = "user_stats"

    # COLUMNS
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True)
    follower_count = db.Column(db.Integer, nullable=False)
    following_count = db.Column(db.Integer, nullable=False)
    post_count = db.Column(db.Integer, nullable=False)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="stats")

    # METHODS
    def __repr__(self):
        return f"<UserStats {self.user_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the UserStats instance into a dictionary representation.
        
        This method converts the UserStats instance into a dictionary representation,
        allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the UserStats instance.
        """
        data = {
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "post_count": self.post_count
        }

        for field in exclude_fields:
            data.pop(field, None)

        return data