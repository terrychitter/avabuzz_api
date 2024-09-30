import datetime
from app import db
from app.utils.id_generation import generate_uuid


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
        profile_accessory_type (str): The type of accessory, indicating its category or purpose which cannot be null.
        profile_type (str): The type of profile for which the accessory is applicable which cannot be null.
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
    __tablename__ = "profile_accessories"

    # COLUMNS
    accessory_id = db.Column(db.String, primary_key=True, default=generate_uuid)
    accessory_name = db.Column(db.String(50), nullable=False)
    accessory_description = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    profile_accessory_type = db.Column(db.String(50), nullable=False)
    profile_type = db.Column(db.String(20), nullable=False)
    ownership_type = db.Column(db.String(20), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    default_accessory = db.Column(db.Boolean, nullable=False, default=False)
    owner_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # RELATIONSHIPS
    owned_accessories = db.relationship(
        "OwnedAccessories", back_populates="profile_accessory"
    )

    # METHODS
    def __repr__(self):
        return f"<ProfileAccessory {self.accessory_id}>"
    
    def to_dict(self, exclude_fields: list = []) -> dict:
        """Converts the ProfileAccessories instance into a dictionary representation.

        This method converts the ProfileAccessories instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the ProfileAccessories instance.
        """
        data = {
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
            data.pop(field, None)

        return data
