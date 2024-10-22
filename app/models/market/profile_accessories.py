from typing import Optional, Union
import uuid
from app import db
from enum import Enum
from datetime import datetime
from app.utils.id_generation import generate_uuid
from app.utils.validation import valid_uuid, valid_enum_element, valid_datetime, valid_string, valid_text, valid_boolean, valid_integer
from sqlalchemy.orm import validates
from sqlalchemy import String, Integer, Boolean, Text, DateTime, Enum as SQLAlchemyEnum
from app.types import OwnershipType, ProfileAccessoryType, ProfileType
from app.types.length import (ACCESSORY_ID_LENGTH,
                              ACCESSORY_NAME_LENGTH_MIN,
                              ACCESSORY_NAME_LENGTH_MAX,
                              MEDIA_URL_LENGTH)

def valid_accessory_id(value: Optional[str]) -> bool:
    """Validates an accessory identifier based on the UUID format.

    Args:
        value (str): The accessory identifier to be validated.

    Returns:
        bool: True if the accessory identifier is valid, False otherwise.
    """
    return valid_uuid(value)

class ProfileAccessories(db.Model): # type: ignore
    """Represents a record of accessories available for user/group profiles.

    This model stores information about various accessories that users/groups can 
    own and use on their profiles. It includes details such as the name, 
    description, and type of the accessory, as well as its availability 
    status and ownership metrics.

    Attributes:
        accessory_id (str): The unique identifier for the accessory, which serves as the primary key. Defaults to a UUID.
        accessory_name (str): The name of the accessory, which cannot be null.
        accessory_description (str): A detailed description of the accessory, which cannot be null.
        media_url (str): The URL pointing to the media representation of the accessory, which cannot be null.
        profile_accessory_type (enum): The type of accessory for the profile which cannot be null.
        profile_type (enum): The type of profile for which the accessory is applicable which cannot be null.
        ownership_type (str): The type of ownership applicable to the accessory (e.g., user, group).
        available (bool): Indicates whether the accessory is currently available for user's to obtain. Defaults to `True`.
        default_accessory (bool): Indicates whether this accessory is an accessory added by default when a user is created. Defaults to `False`.
        owner_count (int): The count of users who own this accessory. Defaults to `0`.
        created_at (datetime): The timestamp when the accessory was created. Defaults to the current time.

    Relationships:
        owned_accessories (OwnedAccessories): A relationship to the OwnedAccessories model, 
                                              indicating which users own this accessory.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "profile_accessories"

    #region COLUMNS
    accessory_id: str = db.Column(String(ACCESSORY_ID_LENGTH), primary_key=True, default=generate_uuid)
    accessory_name: str = db.Column(String(ACCESSORY_NAME_LENGTH_MAX), nullable=False)
    accessory_description: str = db.Column(Text, nullable=False)
    media_url: str = db.Column(String(MEDIA_URL_LENGTH), nullable=False)
    profile_accessory_type: ProfileAccessoryType = db.Column(SQLAlchemyEnum(ProfileAccessoryType), nullable=False)
    profile_type: ProfileType = db.Column(SQLAlchemyEnum(ProfileType), nullable=False)
    ownership_type: OwnershipType = db.Column(SQLAlchemyEnum(OwnershipType), nullable=False)
    available: bool = db.Column(Boolean, nullable=False, default=True)
    default_accessory: bool = db.Column(Boolean, nullable=False, default=False)
    owner_count: int = db.Column(Integer, nullable=False, default=0)
    created_at: datetime = db.Column(DateTime, nullable=False, default=datetime.now)
    #endregion

    #region RELATIONSHIPS
    owned_accessories = db.relationship(
        "OwnedAccessories", back_populates="profile_accessory"
    )

    #region VALIDATION
    # ACCESSORY_ID
    @validates("accessory_id")
    def validate_accessory_id(self, key, accessory_id: str) -> str:
        if not valid_accessory_id(accessory_id):
            raise ValueError("Invalid accessory identifier.")
        return accessory_id
    
    # ACCESSORY_NAME
    @validates("accessory_name")
    def validate_accessory_name(self, key, accessory_name: str) -> str:
        if not valid_string(accessory_name, length=(ACCESSORY_NAME_LENGTH_MIN, ACCESSORY_NAME_LENGTH_MAX), allow_empty=False):
            raise ValueError(f"Invalid accessory name.")
        return accessory_name

    # ACCESSORY_DESCRIPTION
    @validates("accessory_description")
    def validate_accessory_description(self, key, accessory_description: str) -> str:
        if not valid_text(accessory_description, limit=False, allow_empty=True):
            raise ValueError("Invalid accessory description.")
        return accessory_description
    
    # MEDIA_URL
    @validates("media_url")
    def validate_media_url(self, key, media_url: str) -> str:
        if not valid_string(media_url, length=(1, MEDIA_URL_LENGTH), allow_empty=False):
            raise ValueError("Invalid media URL.")
        return media_url

    # PROFILE_ACCESSORY_TYPE
    @validates("profile_accessory_type")
    def validate_profile_accessory_type(self, key, profile_accessory_type: Union[ProfileAccessoryType, str]) -> str:
        if not valid_enum_element(profile_accessory_type, ProfileAccessoryType):
            raise ValueError("Invalid profile accessory type.")
        return ProfileAccessoryType(profile_accessory_type).value

    # PROFILE_TYPE
    @validates("profile_type")
    def validate_profile_type(self, key, profile_type: Union[ProfileType, str]) -> str:
        if not valid_enum_element(profile_type, ProfileType):
            raise ValueError("Invalid profile type.")
        return ProfileType(profile_type).value


    # OWNERSHIP_TYPE
    @validates("ownership_type")
    def validate_ownership_type(self, key, ownership_type: Union[OwnershipType, str]) -> str:
        if not valid_enum_element(ownership_type, OwnershipType):
            raise ValueError("Invalid ownership type.")
        return OwnershipType(ownership_type).value
        
    
    # AVAILABLE
    @validates("available")
    def validate_available(self, key, available: bool) -> bool:
        if not valid_boolean(available):
            raise ValueError("Invalid availability status.")
        return available


    # DEFAULT_ACCESSORY
    @validates("default_accessory")
    def validate_default_accessory(self, key, default_accessory: bool) -> bool:
        if not valid_boolean(default_accessory):
            raise ValueError("Invalid default accessory status.")
        return default_accessory
    
    # OWNER_COUNT
    @validates("owner_count")
    def validate_owner_count(self, key, owner_count: int) -> int:
        if not valid_integer(owner_count, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid owner count.")
        return owner_count

    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created-at timestamp.")
        return created_at
    #endregion

    # METHODS
    def __repr__(self):
        return f"<PROFILE ACCESSORY ID {self.accessory_id}>"
    
    #region TO_DICT
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the ProfileAccessories model."""
        ID = "id"
        NAME = "name"
        DESCRIPTION = "description"
        URL = "url"
        ACCESSORY_TYPE = "accessory_type"
        PROFILE_TYPE = "profile_type"
        OWNERSHIP_TYPE = "ownership_type"
        AVAILABLE = "available"
        DEFAULT_ACCESSORY = "default_accessory"
        OWNER_COUNT = "owner_count"
        CREATED_AT = "created_at"
    
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
        """Converts the ProfileAccessories instance into a dictionary representation.

        This method converts the ProfileAccessories instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the ProfileAccessories instance.
        """
        data: dict = {
            "id": self.accessory_id,
            "name": self.accessory_name,
            "description": self.accessory_description,
            "url": self.media_url,
            "accessory_type": self.profile_accessory_type,
            "profile_type": self.profile_type,
            "ownership_type": self.ownership_type,
            "available": self.available,
            "default_accessory": self.default_accessory,
            "owner_count": self.owner_count,
            "created_at": self.created_at
        }

        for field in exclude_fields:
            data.pop(field.value, None)

        return data
