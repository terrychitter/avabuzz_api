import random
import string
import uuid
from typing import Optional
from sqlalchemy.orm import scoped_session

def generate_unique_public_id(session: scoped_session) -> str:
    """
    Generates a unique public id for a user. It will check if the generated public ID already exists in the database.
    NOTE: This will not add the generated public id to the database. This is the responsibility of the caller.

    Args:
        session (Session): SQLAlchemy session to use for querying the database.

    Returns:
        str: A unique public ID.
    """
    from app.models.user import UserPublicId
    letters = string.ascii_uppercase
    numbers = string.digits
    
    while True:
        random_id = ''.join(random.choice(letters + numbers) for _ in range(3))
        random_id += '-' + ''.join(random.choice(letters + numbers) for _ in range(3))
        
        # Check if the generated ID already exists in the database
        existing_id = session.query(UserPublicId).filter_by(public_id=random_id).first()
        
        if not existing_id:
            return random_id
        
def generate_unique_private_id(session: scoped_session) -> str:
    """
    Generates a unique private ID for a user. It will check if the generated private ID already exists in the database.
    NOTE: This will not add the generated private ID to the database. This is the responsibility of the caller.

    Args:
        session (Session): SQLAlchemy session to use for querying the database.

    Returns:
        str: A unique private ID.
    """
    from app.models import UserPrivateId
    letters = string.ascii_uppercase
    numbers = string.digits
    
    while True:
        random_id: str = ''.join(random.choice(letters + numbers) for _ in range(10))
        
        # Check if the generated ID already exists in the database
        existing_id: Optional[UserPrivateId] = session.query(UserPrivateId).filter_by(private_id=random_id).first()
        
        if not existing_id:
            return random_id

def generate_uuid() -> str:
    """
    Generates a UUID.
    Example: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

    Returns:
        str: A UUID.
    """
    return str(uuid.uuid4())
        
