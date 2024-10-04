from enum import Enum
from app import db
from datetime import datetime

class UserGroups(db.Model): # type: ignore
    """Represents a record of user-created groups within the system.

    This model stores information about groups that users can create and 
    manage. It includes details such as the group's name, description, 
    ownership, and creation date.

    Attributes:
        private_group_id (int): The unique identifier for the group, which serves as the primary key.
        public_group_id (str): The public identifier for the group, which must be unique and cannot be null.
        group_name (str): The name of the group, which cannot be null.
        group_description (str, optional): A detailed description of the group, which can be null.
        created_at (datetime): The timestamp when the group was created. Defaults to the current time.
        owner_id (str): The unique identifier for the user who owns the group, linked to the `users` table. 
                        This cannot be null.

    Relationships:
        owner (Users): A relationship to the Users model, indicating the user who owns the group.
        posts (Posts): A relationship to the Posts model, indicating the posts associated with this group.

    Returns:
        None
    """
    #  TABLE NAME
    __tablename__: str = "user_groups"

    # COLUMNS
    private_group_id: int = db.Column(db.Integer, primary_key=True)
    public_group_id: str = db.Column(db.String(10), nullable=False, unique=True)
    group_name: str = db.Column(db.String(20), nullable=False)
    group_description: str = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    owner_id: str = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)

    # Define the relationship to the Users model
    owner = db.relationship("Users", back_populates="groups")

    # Define the relationship to the Posts model
    posts = db.relationship("Posts", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserGroup {self.private_group_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the UserGroups model."""
        ID = "id"
        NAME = "name"
        DESCRIPTION = "description"
        CREATED_AT = "created_at"
        OWNER = "owner"
        POSTS = "posts"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the UserGroups instance into a dictionary representation.

        This method converts the UserGroups instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the UserGroups instance.
        """
        posts = getattr(self, "posts", [])

        data: dict = {
            "id": self.public_group_id,
            "name": self.group_name,
            "description": self.group_description,
            "created_at": self.created_at,
            "owner": self.owner.to_dict(),
            "posts": [post.to_dict() for post in posts]
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data