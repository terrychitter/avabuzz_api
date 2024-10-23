from enum import Enum
from app import db
from datetime import datetime
from sqlalchemy.orm import validates
from app.utils.id_generation import generate_uuid
from app.utils.validation import valid_uuid, valid_datetime
from app.models.user.users import valid_private_user_id
from app.types.length import (
    BLOCKED_USERS_ID_LENGTH,
    USER_PRIVATE_ID_LENGTH
)

def valid_blocked_users_id(value: str) -> bool:
    """Validates a blocked user identifier based on the UUID format.

    Args:
        value (str): The blocked user identifier to be validated.

    Returns:
        bool: True if the blocked user identifier is valid, False otherwise.
    """
    return valid_uuid(value)

class BlockedUsers(db.Model): # type: ignore
    """Represents a record of users who have blocked each other in the system.

        This model tracks relationships between users who block each other,
        including details on who blocked whom and when the block occurred.

        Attributes:
            `blocked_users_id` (str): The unique identifier for the blocked user record.
            `blocker_id` (str): The unique identifier for the user who initiated the block.
            `blocked_id` (str): The unique identifier for the user who is being blocked.
            `blocked_at` (datetime): The timestamp when the block was initiated.

        Relationships:
            `blocker` (Users): The user who blocked another user.
            `blocked` (Users): The user who is blocked by another user.

        Methods:
            `to_dict(exclude_fields=[])`: Converts the BlockedUsers instance into a dictionary 
                representation, allowing for exclusion of specified fields.

        Returns:
            `None`
    """
    # TABLE NAME
    __tablename__: str = "blocked_users"

    # COLUMNS
    blocked_users_id: str = db.Column(db.String(BLOCKED_USERS_ID_LENGTH), primary_key=True, default=generate_uuid)
    blocker_id: str = db.Column(db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=False)
    blocked_id: str= db.Column(db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=False)
    blocked_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Define the relationship between the BlockedUsers and Users models
    blocker = db.relationship("Users", foreign_keys=[blocker_id])
    blocked = db.relationship("Users", foreign_keys=[blocked_id])

    #region VALIDATION
    # BLOCKED_USERS_ID
    @validates("blocked_users_id")
    def validate_blocked_users_id(self, key: str, blocked_users_id: str) -> str:
        if not valid_blocked_users_id(blocked_users_id):
            raise ValueError("Invalid blocked users identifier.")
        return blocked_users_id
    
    # BLOCKER_ID
    @validates("blocker_id")
    def validate_blocker_id(self, key: str, blocker_id: str) -> str:
        if not valid_private_user_id(blocker_id):
            raise ValueError("Invalid blocker identifier.")
        return blocker_id
    
    # BLOCKED_ID
    @validates("blocked_id")
    def validate_blocked_id(self, key: str, blocked_id: str) -> str:
        if not valid_private_user_id(blocked_id):
            raise ValueError("Invalid blocked identifier.")
        return blocked_id
    
    # BLOCKED_AT
    @validates("blocked_at")
    def validate_blocked_at(self, key: str, blocked_at: datetime) -> datetime:
        if not valid_datetime(blocked_at):
            raise ValueError("Invalid blocked at timestamp.")
        return blocked_at
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<BlockedUsers {self.blocked_users_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the BlockedUsers model."""
        ID = "id"
        BLOCKER = "blocker"
        BLOCKED = "blocked"
        BLOCKED_AT = "blocked_at"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the BlockedUsers instance into a dictionary representation.

        This method converts the BlockedUsers instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the BlockedUsers instance.
        """
        data: dict = {
            "blocked_users_id": self.blocked_users_id,
            "blocker": self.blocker.to_dict(),
            "blocked": self.blocked.to_dict(),
            "blocked_at": self.blocked_at
        }
    
        for field in exclude_fields:
            data.pop(field.value, None)
    
        return data