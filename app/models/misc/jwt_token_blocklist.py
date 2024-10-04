from app import db
from datetime import datetime
from enum import Enum
from app.utils.id_generation import generate_uuid


class JWTTokenBlocklist(db.Model): # type: ignore
    """Represents a record of JWT tokens that have been blacklisted.

    This model tracks JWT tokens that are no longer valid and should be 
    rejected by the authentication system. It stores information about 
    the token identifier and the time when the token was created.

    Attributes:
        jwt_token_blocklist_id (int): The unique identifier for the token blocklist record. Defaults to a UUID.
        jti (str): The JWT identifier, which uniquely identifies the token being blocked and cannot be null.
        created_at (datetime): The timestamp when the token was created and added to the blocklist.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__: str = "jwt_token_blocklist"

    # COLUMNS
    jwt_token_blocklist_id: str = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    jti: str = db.Column(db.String(255), nullable=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # METHODS
    def __repr__(self):
        return f"<Token {self.jti}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the JWTTokenBlocklist model."""
        ID = "id"
        JTI = "jti"
        CREATED_AT = "created_at"
    
    def to_dict(self, exclude_fields: list = [DictKeys]) -> dict:
        """Converts the JWTTokenBlocklist instance into a dictionary representation.

        This method converts the JWTTokenBlocklist instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the JWTTokenBlocklist instance.
        """
        data: dict = {
            "id": self.jwt_token_blocklist_id,
            "jti": self.jti,
            "created_at": self.created_at
        }
        
        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data

    
