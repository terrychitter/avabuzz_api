from app import db
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum

class Users(db.Model): # type: ignore
    """Represents a user account in the system.

    This model stores essential information about users, including their 
    personal details, account settings, and relationships with other users 
    (e.g., followers, groups).

    Attributes:
        private_user_id (str): The unique identifier for the user, serving as the primary key. 
        public_user_id (str): The public identifier for the user, which must be unique and cannot be null.
        username (str): The username chosen by the user, which must be unique and cannot be null.
        email (str): The email address of the user, which must be unique and cannot be null.
        friend_code (str, optional): A unique code for adding friends, which can be null.
        password_hash (str): The hashed password of the user, which cannot be null.
        profile_picture_url (str, optional): A URL pointing to the user's profile picture, defaults to a placeholder image.
        gender (str, optional): The gender of the user, which can be null.
        country (str, optional): The country of the user, which can be null.
        orientation (str, optional): The sexual orientation of the user, which can be null.
        biography (str, optional): A brief biography about the user, which can be null.
        user_type (UserType): The type of user (e.g., user, admin, moderator), which cannot be null and defaults to 'user'.
        birthdate (date, optional): The birthdate of the user, which can be null.
        created_at (datetime): The timestamp when the user account was created. Defaults to the current time.

    Relationships:
        stats (UserStats): A relationship to the UserStats model, indicating the user's statistics.
        active_profile_accessories (UserProfileAccessories): A relationship to the UserProfileAccessories model, indicating the user's active profile accessories.
        posts (Posts): A relationship to the Posts model, indicating the posts created by the user.
        groups (UserGroups): A relationship to the UserGroups model, indicating the groups owned by the user.
        followers (UserFollowers): A relationship to the UserFollowers model, indicating users following this user.
        following (UserFollowers): A relationship to the UserFollowers model, indicating users that this user is following.
        post_reactions (PostReactions): A relationship to the PostReactions model, indicating the user's reactions to posts.
        comments (PostComments): A relationship to the PostComments model, indicating the comments made by the user.
        comment_likes (PostCommentLikes): A relationship to the PostCommentLikes model, indicating the likes given by the user to comments.
        blocked_users (BlockedUsers): A relationship to the BlockedUsers model, indicating users blocked by this user.

    Returns:
        None
    """
    class UserType(Enum):
        user = "user"
        admin = "admin"
        moderator = "moderator"

    __tablename__ = "users"
    private_user_id = db.Column(db.String(10), primary_key=True, nullable=False)
    public_user_id = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    friend_code = db.Column(db.String(10), nullable=True, default=None)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture_url = db.Column(db.String(255), nullable=True, default="https://placehold.co/400")
    gender = db.Column(db.String(20), nullable=True, default=None)
    country = db.Column(db.String(255), nullable=True, default=None)
    orientation = db.Column(db.String(20), nullable=True, default=None)
    biography = db.Column(db.Text, nullable=True)
    user_type = db.Column(SQLAlchemyEnum(UserType), nullable=False, default=UserType.user)
    birthdate = db.Column(db.Date, nullable=True, default=None)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    # Define relationship to UserStats model
    stats = db.relationship("UserStats", uselist=False, back_populates="user", cascade="all, delete-orphan")
    active_profile_accessories = db.relationship(
        "UserProfileAccessories", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Define relationship to Posts model
    posts = db.relationship("Posts", back_populates="user", cascade="all, delete-orphan")

    # Define relationship to UserGroups model
    groups = db.relationship("UserGroups", back_populates="owner")

    # Define relationship to UserFollowers model
    followers = db.relationship(
        "UserFollowers", foreign_keys="[UserFollowers.follower_user_id]", back_populates="followee", cascade="all, delete-orphan", uselist=True
    )

    following = db.relationship(
        "UserFollowers", foreign_keys="[UserFollowers.followee_user_id]", back_populates="follower", cascade="all, delete-orphan", uselist=True
    )

    # Define relationship to PostReactions model
    post_reactions = db.relationship("PostReactions", back_populates="user", cascade="all, delete-orphan")

    # Define relationship to PostComments model
    comments = db.relationship("PostComments", back_populates="user", cascade="all, delete-orphan")

    # Define relationship to PostCommentLikes model
    comment_likes = db.relationship("PostCommentLikes", back_populates="user", cascade="all, delete-orphan")

    # Define relationship to BlockedUsers model
    blocked_users = db.relationship("BlockedUsers", foreign_keys="[BlockedUsers.blocker_id]", back_populates="blocker", cascade="all, delete-orphan", uselist=True)

    def __repr__(self):
        return f"<User {self.private_user_id}>"

    def to_dict(self, exclude_fields=[]):
        """Converts the Users instance into a dictionary representation.

        This method converts the Users instance into a dictionary representation,
        allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the Users instance.
        """
        user_stats = self.stats or {}
        active_profile_accessories = self.active_profile_accessories

        # Initialize variables to hold media URLs
        active_banner_url = None
        active_profile_picture_border_url = None
        active_badge_url = None

        if active_profile_accessories:
            active_banner_url = (
                active_profile_accessories.active_banner.profile_accessory.media_url
                if active_profile_accessories.active_banner
                else None
            )
            active_profile_picture_border_url = (
                active_profile_accessories.active_profile_picture_border.profile_accessory.media_url
                if active_profile_accessories.active_profile_picture_border
                else None
            )
            active_badge_url = (
                active_profile_accessories.active_badge.profile_accessory.media_url
                if active_profile_accessories.active_badge
                else None
            )

        data = {
            "public_user_id": self.public_user_id,
            "username": self.username,
            "email": self.email,
            "friend_code": self.friend_code,
            "profile_picture_url": self.profile_picture_url,
            "gender": self.gender,
            "country": self.country,
            "orientation": self.orientation,
            "biography": self.biography,
            "user_type": self.user_type.value,
            "birth_date": self.birthdate,
            "created_at": self.created_at,
            "user_stats": user_stats.to_dict(),
            "active_accessories": {
                "active_banner_url": active_banner_url,
                "active_profile_picture_border_url": active_profile_picture_border_url,
                "active_badge_url": active_badge_url,
            },
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data
