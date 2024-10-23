from enum import Enum
from sqlalchemy.orm import validates
from app import db
from app.models.user.users import valid_public_user_id
from app.types.length import (
    USER_PUBLIC_ID_LENGTH
)


class UserPublicId(db.Model): # type: ignore
    """
    Represents a record of unique public identifiers for users.

    This model stores unique public identifiers that are assigned to users
    for identification purposes. These identifiers are used to link users to
    various records and relationships within the system.

    Attributes:
        public_id (str): The unique public identifier for the user. This serves as the primary key.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "user_public_ids"

    # COLUMNS
    public_id: str = db.Column(db.String(USER_PUBLIC_ID_LENGTH), primary_key=True)

    #region VALIDATION
    # PUBLIC ID
    @validates("public_id")
    def validate_public_id(self, key, public_id: str) -> str:
        if not valid_public_user_id(public_id):
            raise ValueError("Invalid user public identifier.")
        return public_id
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<UserPublicId {self.public_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the UserPublicId model."""
        ID = "id"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the UserPublicId instance into a dictionary representation.
        
        This method converts the UserPublicId instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the UserPublicId instance.
        """
        data: dict = {
            "id": self.public_id
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data

