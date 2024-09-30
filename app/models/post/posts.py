import datetime
from app import db
from enum import Enum
from app.utils.id_generation import generate_uuid
from sqlalchemy import Enum as SQLAlchemyEnum

class Posts(db.Model): # type: ignore
    """Represents a record of user posts in the database.

    This model stores records of user posts, which can be of different types
    such as text posts, image posts, video posts, or event posts. Each post
    is associated with a specific category and can contain multiple hashtags.

    Attributes:
        post_id (str): The unique identifier for the post, which serves as the primary key. Defaults to a generated UUID.
        post_caption (str, optional): The caption or text content of the post, which can be null.
        post_type (PostType): The type of the post, which is an enumeration of post types. This cannot be null.
        post_category_id (int): The unique identifier for the post category, linked to the `post_categories` table. This cannot be null.
        user_id (str, optional): The unique identifier for the user who created the post, linked to the `users` table. This can be null for group posts.
        group_id (str, optional): The unique identifier for the group to which the post belongs, linked to the `user_groups` table. This can be null for user posts.
        view_count (int): The number of views or interactions on the post. Defaults to 0.
        created_at (datetime): The timestamp when the post was created. Defaults to the current time.

    Relationships:
        post_category (PostCategories): A relationship to the PostCategories model, indicating the category of the post.
        post_hashtags (PostHashTags): A relationship to the PostHashTags model, indicating the hashtags associated with the post.
        hashtags (HashTags): A relationship to the HashTags model, indicating the hashtags associated with the post.
        media (PostMedia): A relationship to the PostMedia model, indicating the media content associated with the post.
        user (Users): A relationship to the Users model, indicating the user who created the post.
        group (UserGroups): A relationship to the UserGroups model, indicating the group to which the post belongs.
        reactions (PostReactionCounts): A relationship to the PostReactionCounts model, indicating the reaction counts on the post.
        post_reactions (PostReactions): A relationship to the PostReactions model, indicating the reactions on the post.
        comments (PostComments): A relationship to the PostComments model, indicating the comments on the post.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "posts"

    class PostType(Enum):
        """Enumeration of post types for the Posts model.

        This enumeration defines the different types of posts that can be created
        by users, including text posts, image posts, video posts, and event posts.

        Attributes:
            post (str): A text-based post with no media content.
            image (str): A post containing an image or photo.
            video (str): A post containing a video.
            event (str): A post indicating an event or activity.
        
        Returns:
            None
        """
        POST = "post"
        IMAGE = "image"
        VIDEO = "video"
        EVENT = "event"
    
    # COLUMNS
    post_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_caption = db.Column(db.Text, nullable=True)
    post_type = db.Column(SQLAlchemyEnum(PostType), nullable=False)
    post_category_id = db.Column(db.Integer, db.ForeignKey("post_categories.post_category_id"), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=True)
    group_id = db.Column(db.String(10), db.ForeignKey("user_groups.private_group_id"), nullable=True)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Define relationship to PostCategories model
    post_category = db.relationship("PostCategories", back_populates="posts")

    # Define relationship to PostHashTags model with cascade
    post_hashtags = db.relationship("PostHashTags", backref="post", cascade="all, delete-orphan")

    # Define relationship to Hashtags model
    hashtags = db.relationship("HashTags", secondary="post_hashtags", back_populates="posts")

    # Define relationship to PostMedia model
    media = db.relationship("PostMedia", back_populates="post", cascade="all, delete-orphan")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="posts")

    # Define relationship to UserGroups model
    group = db.relationship("UserGroups", back_populates="posts")

    # Define relationship to PostReactionCounts model
    reactions = db.relationship("PostReactionCounts", back_populates="post", cascade="all, delete-orphan")

    # Define relationship to PostReactionTypes model
    post_reactions = db.relationship("PostReactions", back_populates="post", cascade="all, delete-orphan")

    # Define relationship to PostComments model
    comments = db.relationship("PostComments", back_populates="post", cascade="all, delete-orphan")

    # METHODS
    def __repr__(self):
        return f"<Post {self.post_id}>"
    
    def to_dict(self, user_id=None, exclude_fields: list = ["user_reacted"]):
        """Converts the Posts instance into a dictionary representation.
        
        This method converts the Posts instance into a dictionary representation,
        allowing for exclusion of specified fields. It also includes additional
        information such as hashtags, media, and reactions.

        Args:
            user_id (str): The unique identifier for the user viewing the post. This is used to fetch the user's reaction.
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the Posts instance.
        """
        post_hashtags_relationship = getattr(self, "post_hashtags", [])
        media_relationship = getattr(self, "media", [])
        reactions_relationship = getattr(self, "reactions", [])
        post_reactions_relationship = getattr(self, "post_reactions", [])
        
        data = {
            "id": self.post_id,
            "caption": self.post_caption,
            "type": self.post_type.value,
            "category": self.post_category.to_dict(),
            "view_count": self.view_count,
            "poster": self.user.to_dict(),
            "created_at": self.created_at,
            "hashtags": [tag.hashtag.to_dict()["name"] for tag in post_hashtags_relationship],
            "media": [media.to_dict() for media in media_relationship],
            "reactions": [reaction.to_dict(exclude_fields=["post_id"]) for reaction in reactions_relationship],
        }
        
        # Check if user_id is provided, to fetch their reaction
        if user_id:
            user_reaction = next((reaction for reaction in post_reactions_relationship if reaction.user_id == user_id), None)
            data["user_reacted"] = bool(user_reaction)  # True if user has reacted, False otherwise
            data["user_reaction_type"] = user_reaction.post_reaction_type if user_reaction else None

        # Remove excluded fields from the dictionary
        for field in exclude_fields:
            data.pop(field, None)
        
        return data
