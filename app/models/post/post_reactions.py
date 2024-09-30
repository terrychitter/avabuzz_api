from app import db

class PostReactions(db.Model): # type: ignore
    """
    Represents a record of reactions on user posts in the database.
    
    This model stores records of reactions on user posts, indicating the users
    who reacted to a specific post. Each reaction is associated with a specific
    post and user, and can be of different types such as likes, dislikes, etc.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        user_id (str): The unique identifier for the user who reacted to the post, linked to the `users` table. This serves as part of the primary key.
        post_reaction_type (str): The type of reaction, linked to the `post_reaction_types` table. This serves as part of the primary key.

    Relationships:
        user (Users): A relationship to the Users model, indicating the user who reacted to the post.
        post (Posts): A relationship to the Posts model, indicating the post associated with the reaction.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_reactions"

    # COLUMNS
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True)
    post_reaction_type = db.Column(db.String(20), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="post_reactions")

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="post_reactions")

    # METHODS
    def __repr__(self):
        return f"<PostReaction {self.post_id}-{self.user_id}-{self.post_reaction_type}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostReactions instance into a dictionary representation.

        This method converts the PostReactions instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostReactions instance.
        """
        data = {
            "post_id": self.post.to_dict(),
            "user_id": self.user.to_dict(),
            "reaction": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data