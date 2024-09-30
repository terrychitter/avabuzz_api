from app import db
from app.utils.id_generation import generate_uuid

class PostCategories(db.Model): # type: ignore
    """Represents a record of post categories in the database.

    This model stores records of post categories, which are used to categorize
    and group user posts by topic. Each post category can have multiple posts.

    Attributes:
        post_category_id (str): The unique identifier for the post category, which serves as the primary key. Defaults to a generated UUID.
        post_category_name (str): The name of the post category. This cannot be null.
        post_category_description (str, optional): The description of the post category. This can be null.
    
    Relationships:
        posts (Posts): A relationship to the Posts model, indicating the posts associated with the category.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_categories"

    # COLUMNS
    post_category_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_category_name = db.Column(db.String(50), nullable=False)
    post_category_description = db.Column(db.Text, nullable=True)

    # Define the relationship to the Posts model
    posts = db.relationship("Posts", back_populates="post_category")

    # METHODS
    def __repr__(self):
        return f"<PostCategory {self.post_category_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """
        Converts the PostCategories instance into a dictionary representation.

        This method converts the PostCategories instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostCategories instance.
        """
        data = {
            "id": self.post_category_id,
            "name": self.post_category_name,
            "description": self.post_category_description
        }

        for field in exclude_fields:
            data.pop(field, None)