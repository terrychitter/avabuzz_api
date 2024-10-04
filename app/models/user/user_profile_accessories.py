from enum import Enum
from app import db

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
        db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True
    )
    active_banner_id: str = db.Column(
        db.String(36),
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )
    active_profile_picture_border_id: str = db.Column(
        db.String(36),
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )
    active_badge_id: str = db.Column(
        db.String(36),
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