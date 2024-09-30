from app import db

class PostReactionTypes(db.Model): # type: ignore
    """Represents a record of reaction types for user posts in the database.

    This model stores the different types of reactions that users can have on
    posts, such as likes, dislikes, etc. Each reaction type is associated with
    a specific post and user.

    Attributes:
        post_reaction_type (str): The unique identifier for the reaction type, which serves as the primary key.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_reaction_types"

    # COLUMNS
    post_reaction_type = db.Column(db.String(20), primary_key=True)

    # METHODS
    def __repr__(self):
        return f"<PostReactionType {self.post_reaction_type}>"
    
    def to_dict(self, exclude_fields: list = []):
        """
        Converts the PostReactionTypes instance into a dictionary representation.

        This method converts the PostReactionTypes instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostReactionTypes instance.
        """
        data = {
            "type": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data