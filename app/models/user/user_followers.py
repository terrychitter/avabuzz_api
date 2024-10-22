from enum import Enum
from app import db
from datetime import datetime
from app.utils.id_generation import generate_uuid

class UserFollowers(db.Model): # type: ignore
    """Represents a record of user follow relationships within the system.

    This model tracks the relationships between users who follow each other, 
    including details on who follows whom and when the follow action occurred.

    Attributes:
        follow_id (int): The unique identifier for the follow record, which serves as the primary key. 
                         Defaults to a generated UUID.
        follower_user_id (int): The unique identifier for the user who is following another user, 
                                linked to the `users` table. This cannot be null.
        followee_user_id (int): The unique identifier for the user who is being followed, 
                                linked to the `users` table. This cannot be null.
        followed_at (datetime): The timestamp when the follow action occurred. Defaults to the current time.

    Relationships:
        follower (Users): A relationship to the Users model, indicating the user who follows another user.
        followee (Users): A relationship to the Users model, indicating the user who is being followed.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "user_followers"

    # COLUMNS
    follow_id: str = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    follower_user_id: str = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    followee_user_id: str = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    followed_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # RELATIONSHIPS
    follower = db.relationship("Users", foreign_keys=[follower_user_id])
    followee = db.relationship("Users", foreign_keys=[followee_user_id])

    # METHODS
    def __repr__(self):
        return f"<UserFollowers {self.id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the UserFollowers model."""
        ID = "id"
        FOLLOWER = "follower"
        FOLLOWEE = "followee"
        FOLLOWED_AT = "followed_at"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the UserFollowers instance into a dictionary representation.

        This method converts the UserFollowers instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the UserFollowers instance.
        """
        data: dict = {
            "id": self.follow_id,
            "follower": self.follower.to_dict(),
            "followee": self.followee.to_dict(),
            "followed_at": self.followed_at
        }
    
        for field in exclude_fields:
            data.pop(field.value, None)
    
        return data