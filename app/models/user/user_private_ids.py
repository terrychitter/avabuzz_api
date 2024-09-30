from app import db

class UserPrivateId(db.Model): # type: ignore
    """Represents a record of unique private identifiers for users.
    
    This model stores unique private identifiers that are assigned to users
    for identification purposes. These identifiers are used to link users to
    various records and relationships within the system.

    Attributes:
        private_id (str): The unique private identifier for the user. This serves as the primary key.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "user_private_ids"

    # COLUMNS
    private_id = db.Column(db.String(10), primary_key=True)

    # METHODS
    def __repr__(self):
        return f"<UserPrivateId {self.private_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the UserPrivateId instance into a dictionary representation.
        
        This method converts the UserPrivateId instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the UserPrivateId instance.
        """
        data = {
            "id": self.private_id
        }

        for field in exclude_fields:
            data.pop(field, None)

        return data

