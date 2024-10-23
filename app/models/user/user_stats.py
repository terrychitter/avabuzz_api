from enum import Enum
from app import db
from sqlalchemy.orm import validates
from app.utils.validation import valid_integer
from app.models.user.users import valid_private_user_id
from app.types.length import (
    USER_PRIVATE_ID_LENGTH
)

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
    __tablename__: str = "user_stats"

    # COLUMNS
    user_id: str = db.Column(db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), primary_key=True)
    follower_count: int = db.Column(db.Integer, nullable=False)
    following_count: int = db.Column(db.Integer, nullable=False)
    post_count: int = db.Column(db.Integer, nullable=False)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="stats")

    #region VALIDATION
    # USER ID
    @validates("user_id")
    def validate_user_id(self, key, user_id: str) -> str:
        if not valid_private_user_id(user_id):
            raise ValueError("Invalid user identifier.")
        return user_id
    
    # FOLLOWER COUNT
    @validates("follower_count")
    def validate_follower_count(self, key, follower_count: int) -> int:
        if not valid_integer(follower_count, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid follower count.")
        return follower_count
    
    # FOLLOWING COUNT
    @validates("following_count")
    def validate_following_count(self, key, following_count: int) -> int:
        if not valid_integer(following_count, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid following count.")
        return following_count
    
    # POST COUNT
    @validates("post_count")
    def validate_post_count(self, key, post_count: int) -> int:
        if not valid_integer(post_count, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid post count.")
        return post_count
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<USERSTATS {self.user_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the UserStats model."""
        USER_ID = "user_id"
        FOLLOWERS = "followers"
        FOLLOWING = "following"
        POSTS = "posts"
    
    def to_dict(self, exclude_fields: list[DictKeys] = [DictKeys.USER_ID]) -> dict:
        """Converts the UserStats instance into a dictionary representation.
        
        This method converts the UserStats instance into a dictionary representation,
        allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the UserStats instance.
        """
        data: dict = {
            "user_id": self.user_id,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "post_count": self.post_count
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data