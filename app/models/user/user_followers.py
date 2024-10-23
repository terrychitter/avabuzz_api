from enum import Enum
from app import db
from datetime import datetime
from sqlalchemy.orm import validates
from app.models.user.users import valid_private_user_id
from app.utils.validation import valid_uuid, valid_datetime
from app.utils.id_generation import generate_uuid
from app.types.length import (
    USER_PRIVATE_ID_LENGTH,
    FOLLOWER_ID_LENGTH
)

def valid_follow_id(value: str) -> bool:
    """Validates a follow identifier based on the UUID format.

    Args:
        value (str): The follow identifier to be validated.

    Returns:
        bool: True if the follow identifier is valid, False otherwise.
    """
    return valid_uuid(value)

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
    follow_id: str = db.Column(db.String(FOLLOWER_ID_LENGTH), primary_key=True, default=generate_uuid)
    follower_user_id: str = db.Column(db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=False)
    followee_user_id: str = db.Column(db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=False)
    followed_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # RELATIONSHIPS
    follower = db.relationship("Users", foreign_keys=[follower_user_id])
    followee = db.relationship("Users", foreign_keys=[followee_user_id])

    #region VALIDATION
    # FOLLOW ID
    @validates("follow_id")
    def validate_follow_id(self, key, follow_id: str) -> str:
        if not valid_follow_id(follow_id):
            raise ValueError("Invalid follow identifier")
        return follow_id
        
    # FOLLOWER USER ID
    @validates("follower_user_id")
    def validate_follower_user_id(self, key, follower_user_id: str) -> str:
        if not valid_private_user_id(follower_user_id):
            raise ValueError("Invalid follower user identifier")
        return follower_user_id
    
    # FOLLOWEE USER ID
    @validates("followee_user_id")
    def validate_followee_user_id(self, key, followee_user_id: str) -> str:
        if not valid_private_user_id(followee_user_id):
            raise ValueError("Invalid followee user identifier")
        return followee_user_id
    
    # FOLLOWED AT
    @validates("followed_at")
    def validate_followed_at(self, key, followed_at: datetime) -> datetime:
        if not valid_datetime(followed_at):
            raise ValueError("Invalid followed at timestamp")
        return followed_at
    #endregion VALIDATION
    
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