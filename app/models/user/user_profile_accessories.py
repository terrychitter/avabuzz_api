from enum import Enum
from app import db
from sqlalchemy.orm import validates
from app.models.user.users import valid_private_user_id
from app.models.user.owned_accessories import valid_owned_accessory_id
from app.types.length import (
    USER_PRIVATE_ID_LENGTH,
    OWNED_ACCESSORY_ID_LENGTH
)

class UserProfileAccessories(db.Model): # type: ignore
    """Represents the active profile accessories for a user account.

    This model stores the active profile accessories for a user, including the active banner,
    profile picture border, and badge.

    Attributes:
        user_id (str): The unique identifier for the user, serving as the primary key.
        active_banner_id (int): The identifier for the active banner accessory, which cannot be null.
        active_profile_picture_border_id (int): The identifier for the active profile picture border accessory, which cannot be null.
        active_badge_id (int): The identifier for the active badge accessory, which cannot be null.
    
    Relationships:
        user (Users): A relationship to the Users model, indicating the user associated with the active profile accessories.
        active_banner (OwnedAccessories): A relationship to the OwnedAccessories model, indicating the active banner accessory.
        active_profile_picture_border (OwnedAccessories): A relationship to the OwnedAccessories model, indicating the active profile picture border accessory.
        active_badge (OwnedAccessories): A relationship to the OwnedAccessories model, indicating the active badge accessory.

    Returns:
        None
    """

    # TABLE NAME
    __tablename__: str = "user_profile_accessories"


    # COLUMNS
    user_id: str = db.Column(
        db.String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), primary_key=True
    )
    active_banner_id: str = db.Column(
        db.String(OWNED_ACCESSORY_ID_LENGTH),
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )
    active_profile_picture_border_id: str = db.Column(
        db.String(OWNED_ACCESSORY_ID_LENGTH),
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )
    active_badge_id: str = db.Column(
        db.String(OWNED_ACCESSORY_ID_LENGTH),
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="active_profile_accessories")

    # Define relationships to OwnedAccessories model
    active_banner = db.relationship(
        "OwnedAccessories",
        foreign_keys=[active_banner_id],
        back_populates="user_profile_accessories_banner",
    )
    active_profile_picture_border = db.relationship(
        "OwnedAccessories",
        foreign_keys=[active_profile_picture_border_id],
        back_populates="user_profile_accessories_border",
    )
    active_badge = db.relationship(
        "OwnedAccessories",
        foreign_keys=[active_badge_id],
        back_populates="user_profile_accessories_badge",
    )

    #region VALIDATION
    # USER_ID
    @validates("user_id")
    def validate_user_id(self, key: str, user_id: str) -> str:
        if not valid_private_user_id(user_id):
            raise ValueError("Invalid user identifier.")
        return user_id
    
    # ACTIVE_BANNER_ID
    @validates("active_banner_id")
    def validate_active_banner_id(self, key: str, active_banner_id: str) -> str:
        if not valid_owned_accessory_id(active_banner_id):
            raise ValueError("Invalid active banner identifier.")
        return active_banner_id
    
    # ACTIVE_PROFILE_PICTURE_BORDER_ID
    @validates("active_profile_picture_border_id")
    def validate_active_profile_picture_border_id(self, key: str, active_profile_picture_border_id: str) -> str:
        if not valid_owned_accessory_id(active_profile_picture_border_id):
            raise ValueError("Invalid active profile picture border identifier.")
        return active_profile_picture_border_id
    
    # ACTIVE_BADGE_ID
    @validates("active_badge_id")
    def validate_active_badge_id(self, key: str, active_badge_id: str) -> str:
        if not valid_owned_accessory_id(active_badge_id):
            raise ValueError("Invalid active badge identifier.")
        return active_badge_id
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<UserProfileAccessories {self.user_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the UserProfileAccessories model."""
        USER_ID = "user_id"
        BANNER = "banner"
        PROFILE_PICTURE_BORDER = "profile_picture_border"
        BADGE = "badge"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []):
        """Converts the UserProfileAccessories instance into a dictionary representation.
        
        This method converts the UserProfileAccessories instance into a dictionary representation,
        allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the UserProfileAccessories instance.
        """
        data = {
            "user_id": self.user_id,
            "banner": self.active_banner.to_dict(),
            "profile_picture_border": self.active_profile_picture_border.to_dict(),
            "badge": self.active_badge.to_dict()
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data