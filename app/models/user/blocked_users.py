from app import db
from datetime import datetime
from app.utils.id_generation import generate_uuid

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
    __tablename__ = "blocked_users"

    # COLUMNS
    blocked_users_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    blocker_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    blocked_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    blocked_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Define the relationship between the BlockedUsers and Users models
    blocker = db.relationship("Users", foreign_keys=[blocker_id])
    blocked = db.relationship("Users", foreign_keys=[blocked_id])

    # METHODS
    def __repr__(self):
        return f"<BlockedUsers {self.blocked_users_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the BlockedUsers instance into a dictionary representation.

        This method converts the BlockedUsers instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the BlockedUsers instance.
        """
        data = {
            "blocked_users_id": self.blocked_users_id,
            "blocker": self.blocker.to_dict(),
            "blocked": self.blocked.to_dict(),
            "blocked_at": self.blocked_at
        }
    
        for field in exclude_fields:
            data.pop(field, None)
    
        return data