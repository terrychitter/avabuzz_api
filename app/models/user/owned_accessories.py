from enum import Enum
from app import db
from datetime import datetime
from sqlalchemy.orm import validates
from app.utils.id_generation import generate_uuid
from app.utils.validation import valid_uuid, valid_datetime
from app.models.market.profile_accessories import valid_accessory_id
from app.models.user.users import valid_private_user_id
from app.types.length import (
    USER_PRIVATE_ID_LENGTH,
    ACCESSORY_ID_LENGTH,
    OWNED_ACCESSORY_ID_LENGTH
)


def valid_owned_accessory_id(value: str) -> bool:
    """Validates an owned accessory identifier based on the UUID format.

    Args:
        value (str): The owned accessory identifier to be validated.

    Returns:
        bool: True if the owned accessory identifier is valid, False otherwise.
    """
    return valid_uuid(value)
class OwnedAccessories(db.Model): # type: ignore
    """Represents a record of accessories owned by users.

    This model tracks accessories that users own, including the user associated 
    with each accessory and the timestamp when the accessory was acquired. It 
    also defines relationships with related models to manage user-specific 
    accessory data.

    Attributes:
        owned_accessory_id (int): The unique identifier for the owned accessory record. Defaults to a UUID.
        user_id (str): The unique identifier for the user who owns the accessory, 
                       linked to the `users` table. This can be null provided a group_id is provided.
        created_at (datetime): The timestamp when the accessory was created/owned. Defaults to the current time.
        accessory_id (str): The unique identifier for the accessory, linked to the 
                            `profile_accessories` table and cannot be null.

    Relationships:
        profile_accessory (ProfileAccessories): A relationship to the ProfileAccessories model,
                                                indicating the accessory details.
        user_profile_accessories_banner (UserProfileAccessories): A relationship for 
            managing the active banner accessory for the user.
        user_profile_accessories_border (UserProfileAccessories): A relationship for 
            managing the active profile picture border accessory for the user.
        user_profile_accessories_badge (UserProfileAccessories): A relationship for 
            managing the active badge accessory for the user.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "owned_accessories"

    # COLUMNS
    owned_accessory_id: str = db.Column(db.String(OWNED_ACCESSORY_ID_LENGTH), primary_key=True, default=generate_uuid)
    user_id: str = db.Column(
        db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=True
    )
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    accessory_id: str = db.Column(
        db.String(ACCESSORY_ID_LENGTH), db.ForeignKey("profile_accessories.accessory_id"), nullable=False
    )

    # Define relationship to ProfileAccessories model
    profile_accessory = db.relationship(
        "ProfileAccessories", back_populates="owned_accessories"
    )

    # Define relationships to UserProfileAccessories model
    user_profile_accessories_banner = db.relationship(
        "UserProfileAccessories",
        foreign_keys="[UserProfileAccessories.active_banner_id]",
        back_populates="active_banner",
    )
    user_profile_accessories_border = db.relationship(
        "UserProfileAccessories",
        foreign_keys="[UserProfileAccessories.active_profile_picture_border_id]",
        back_populates="active_profile_picture_border",
    )
    user_profile_accessories_badge = db.relationship(
        "UserProfileAccessories",
        foreign_keys="[UserProfileAccessories.active_badge_id]",
        back_populates="active_badge",
    )

    #region VALIDATION
    # OWNED_ACCESSORY_ID
    @validates("owned_accessory_id")
    def validate_owned_accessory_id(self, key: str, owned_accessory_id: str) -> str:
        if not valid_owned_accessory_id(owned_accessory_id):
            raise ValueError("Invalid owned accessory identifier.")
        return owned_accessory_id
    
    # USER_ID
    @validates("user_id")
    def validate_user_id(self, key: str, user_id: str) -> str:
        if not valid_private_user_id(user_id):
            raise ValueError("Invalid user identifier.")
        return user_id
    
    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key: str, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created at timestamp.")
        return created_at
    
    # ACCESSORY_ID
    @validates("accessory_id")
    def validate_accessory_id(self, key: str, accessory_id: str) -> str:
        if not valid_accessory_id(accessory_id):
            raise ValueError("Invalid accessory identifier.")
        return accessory_id

    # METHODS
    def __repr__(self):
        return f"<OwnedAccessories {self.owned_accessory_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the OwnedAccessories model."""
        ID = "id"
        USER_ID = "user_id"
        CREATED_AT = "created_at"
        ACCESSORY = "accessory"
    
    def to_dict(self, exclude_fields: list[DictKeys] = [DictKeys.USER_ID]) -> dict:
        """Converts the OwnedAccessories instance into a dictionary representation.

        This method converts the OwnedAccessories instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the OwnedAccessories instance.
        """
        data: dict = {
            "id": self.owned_accessory_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "accessory": self.profile_accessory.to_dict(),
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data
