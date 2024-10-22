from typing import Optional
import uuid
from app import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import String, DateTime
from app.utils.id_generation import generate_uuid
from app.utils.validation import valid_uuid, valid_datetime
from app.types.length import (JWT_TOKEN_BLOCKLIST_ID_LENGTH,
                              JTI_LENGTH)

# ----------------- VALIDATE JWT TOKEN BLOCKLIST ID ----------------- #
def valid_jwt_token_blocklist_id(value: Optional[str]) -> bool:
    """
    Validates a JWT token blocklist identifier based on the UUID format.

    Args:
        value (str): The JWT token blocklist identifier to be validated.

    Returns:
        bool: True if the JWT token blocklist identifier is valid, False otherwise.
    """
    return valid_uuid(value)

# ----------------- VALIDATE JTI ----------------- #
def valid_jti(value: Optional[str]) -> bool:
    """
    Validates a JWT identifier based on the UUID format.

    Args:
        value (str): The JWT identifier to be validated.

    Returns:
        bool: True if the JWT identifier is valid, False otherwise.
    """
    return valid_uuid(value)

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
    jwt_token_blocklist_id: str = db.Column(String(JWT_TOKEN_BLOCKLIST_ID_LENGTH), primary_key=True, default=generate_uuid)
    jti: str = db.Column(db.String(JTI_LENGTH), nullable=False)
    created_at: datetime = db.Column(DateTime, nullable=False, default=datetime.now)

    #region VALIDATION
    # JWT_TOKEN_BLOCKLIST_ID
    @validates("jwt_token_blocklist_id")
    def validate_jwt_token_blocklist_id(self, key, jwt_token_blocklist_id: str) -> str:
        if not valid_jwt_token_blocklist_id(jwt_token_blocklist_id):
            raise ValueError("Invalid JWT token blocklist identifier.")
        return jwt_token_blocklist_id

    # JTI
    @validates("jti")
    def validate_jti(self, key, jti: str) -> str:
        if not valid_jti(jti):
            raise ValueError("Invalid JWT identifier.")
        return jti
    
    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created-at timestamp.")
        return created_at
    #endregion VALIDATION

    # METHODS
    def __repr__(self):
        return f"<JWT_TOKEN_BLOCKLIST_ID {self.jwt_token_blocklist_id}>"
    
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the JWTTokenBlocklist model."""
        ID = "id"
        JTI = "jti"
        CREATED_AT = "created_at"
    
    #region TO_DICT
    def to_dict(self, exclude_fields: list[DictKeys] = []) -> dict:
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
    #endregion TO_DICT

    
