from app import db
from enum import Enum
from datetime import datetime
from typing import Optional, Union
from app.types.enum import PostType
from sqlalchemy.orm import validates
from app.utils.validation import valid_uuid, valid_enum_element, valid_datetime, valid_integer
from app.models.post.post_categories import valid_post_category_id
from app.models.user.users import valid_private_user_id
from app.utils.id_generation import generate_uuid
from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, Integer, String, Text
from app.types.length import (
    POST_ID_LENGTH,
    POST_CATEGORY_ID_LENGTH,
    USER_PRIVATE_ID_LENGTH,
    USER_GROUP_PRIVATE_ID_LENGTH
)

def valid_post_id(value: Optional[str]) -> bool:
    """Validates a post identifier based on the UUID format.

    Args:
        value (str): The post identifier to be validated.

    Returns:
        bool: True if the post identifier is valid, False otherwise.
    """
    return valid_uuid(value)

class Posts(db.Model): # type: ignore
    """Represents a record of user posts in the database.

    This model stores records of user posts, which can be of different types
    such as text posts, image posts, video posts, or event posts. Each post
    is associated with a specific category and can contain multiple hashtags.

    Attributes:
        post_id (str): The unique identifier for the post, which serves as the primary key. Defaults to a generated UUID.
        post_caption (str, optional): The caption or text content of the post, which can be null.
        post_type (PostType): The type of the post, which is an enumeration of post types. This cannot be null.
        post_category_id (str): The unique identifier for the post category, linked to the `post_categories` table. This cannot be null.
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
    __tablename__: str = "posts"
    
    # COLUMNS
    post_id: str = db.Column(String(POST_ID_LENGTH), primary_key=True, default=generate_uuid)
    post_caption: str = db.Column(Text, nullable=True)
    post_type: PostType = db.Column(SQLAlchemyEnum(PostType), nullable=False)
    post_category_id: str = db.Column(String(POST_CATEGORY_ID_LENGTH), db.ForeignKey("post_categories.post_category_id"), nullable=False)
    user_id: str = db.Column(String(USER_PRIVATE_ID_LENGTH), db.ForeignKey("users.private_user_id"), nullable=True)
    group_id: str = db.Column(String(USER_GROUP_PRIVATE_ID_LENGTH), db.ForeignKey("user_groups.private_group_id"), nullable=True)
    view_count: int = db.Column(Integer, nullable=False, default=0)
    created_at: datetime = db.Column(DateTime, nullable=False, default=datetime.now)

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

    #region VALIDATION
    # POST_ID
    @validates("post_id")
    def validate_post_id(self, key, post_id: str) -> str:
        if not valid_post_id(post_id):
            raise ValueError("Invalid post ID.")
        return post_id
    
    # POST_TYPE
    @validates("post_type")
    def validate_post_type(self, key, post_type: Union[PostType, str]) -> str:
        if not valid_enum_element(post_type, PostType):
            raise ValueError("Invalid post type.")
        return PostType(post_type).value
    
    # POST_CATEGORY_ID
    @validates("post_category_id")
    def validate_post_category_id(self, key, post_category_id: str) -> str:
        if not valid_post_category_id(post_category_id):
            raise ValueError("Invalid post category ID.")
        return post_category_id

    
    # USER_ID
    @validates("user_id")
    def validate_user_id(self, key, user_id: str) -> str:
        if not valid_private_user_id(user_id):
            raise ValueError("Invalid user ID.")
        return user_id
    
    # GROUP_ID
    # TODO: Add validation for group_id

    # VIEW_COUNT
    @validates("view_count")
    def validate_view_count(self, key, view_count: int) -> int:
        if not valid_integer(view_count, allow_negative=False, allow_zero=True):
            raise ValueError("Invalid view count.")
        return view_count

    
    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created at datetime.")
        return created_at
    #endregion VALIDATION
    
    # METHODS
    def __repr__(self):
        return f"<Post {self.post_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the Posts model."""
        ID = "id"
        CAPTION = "caption"
        TYPE = "type"
        CATEGORY = "category"
        VIEW_COUNT = "view_count"
        POSTER = "poster"
        CREATED_AT = "created_at"
        HASHTAGS = "hashtags"
        MEDIA = "media"
        REACTIONS = "reactions"
        USER_REACTED = "user_reacted"
        USER_REACTION_TYPE = "user_reaction_type"
    
    def to_dict(self, user_id: Optional[str] = None, exclude_fields: list[DictKeys] = [DictKeys.USER_REACTED]) -> dict:
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
        
        data: dict = {
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
            data.pop(field.value, None)
        
        return data
