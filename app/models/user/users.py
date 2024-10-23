from typing import Optional, Union
from app import db
import re
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from datetime import datetime, date
from app.utils.id_generation import generate_uuid
from app.types.length import USER_PRIVATE_ID_LENGTH
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum
from app.types.enum import UserType
from app.utils.validation import (
    valid_uuid,
    valid_string,
    valid_email,
    valid_text,
    valid_datetime,
    valid_enum_element
    )
from app.types.length import (
    USER_PRIVATE_ID_LENGTH,
    USER_PUBLIC_ID_LENGTH,
    USER_USERNAME_LENGTH_MIN,
    USER_BIOGRAPHY_TEXT_LIMIT,
    USER_USERNAME_LENGTH_MAX,
    USER_EMAIL_LENGTH,
    USER_PASSWORD_HASH_LENGTH,
    USER_USERNAME_LENGTH_MAX,
    USER_PROFILE_PICTURE_URL_LENGTH,
    USER_FRIEND_CODE_LENGTH,
    USER_GENDER_LENGTH,
    USER_COUNTRY_LENGTH,
    USER_ORIENTATION_LENGTH,
)

def valid_private_user_id(value: Optional[str]) -> bool:
    """
    Validates a user's private identifier.

    Args:
        value (str): The user identifier to be validated.

    Returns:
        bool: True if the user identifier is valid, False otherwise.
    """
    return valid_uuid(value)

def valid_public_user_id(value: Optional[str]) -> bool:
    """
    Validates a user's public identifier.

    Args:
        value (str): The user identifier to be validated.

    Returns:
        bool: True if the user identifier is valid, False otherwise
    """
    if value is None:
        return False
    p = r'^[A-Z0-9]{3}-[A-Z0-9]{3}$'
    return bool(re.match(p, value))

def valid_friend_code(value: Optional[str]) -> bool:
    """
    Validates a friend code based on a simple regex pattern.
    Valid Friend Code Format: **XXX-XXX**, where X is a digit or letter.
    Friend Codes may be null.

    Args:
        value (str): The friend code to be validated.
    
    Returns:
        bool: True if the friend code is valid, False otherwise.
    """
    if value is None:
        return True
    p = r'^[A-Z0-9]{3}-[A-Z0-9]{3}$'
    return bool(re.match(p, value))

def valid_password_hash(value: Optional[str]) -> bool:
    """
    Validates a password hash based on the scrypt format.

    Args:
        value (str): The password hash to be validated.

    Returns:
        bool: True if the password hash is valid, False otherwise.
    """
    if value is None:
        return False
    p = (
        r'^scrypt:(\d+):(\d+):(\d+)\$'        # scrypt parameters (N:r:p)
        r'[A-Za-z0-9+/]{16}\$'                # 16-character base64 salt
        r'[a-f0-9]{128}$'                     # 128-character hex hash
    )
    return bool(re.match(p, value))

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

    __tablename__ = "users"
    private_user_id: str = db.Column(db.String(USER_PRIVATE_ID_LENGTH), primary_key=True, nullable=False, default=generate_uuid)
    public_user_id: str = db.Column(db.String(USER_PUBLIC_ID_LENGTH), unique=True, nullable=False)
    username: str = db.Column(db.String(USER_USERNAME_LENGTH_MAX), unique=True, nullable=False)
    email: str = db.Column(db.String(USER_EMAIL_LENGTH), unique=True, nullable=False)
    friend_code: str = db.Column(db.String(USER_FRIEND_CODE_LENGTH), nullable=True, default=None)
    password_hash: str = db.Column(db.String(USER_PASSWORD_HASH_LENGTH), nullable=False)
    profile_picture_url: str = db.Column(db.String(USER_PROFILE_PICTURE_URL_LENGTH), nullable=True, default="https://placehold.co/400")
    gender: str = db.Column(db.String(USER_GENDER_LENGTH), nullable=True, default=None)
    country: str = db.Column(db.String(USER_COUNTRY_LENGTH), nullable=True, default=None)
    orientation: str = db.Column(db.String(USER_ORIENTATION_LENGTH), nullable=True, default=None)
    biography: str = db.Column(db.Text, nullable=True)
    user_type: UserType = db.Column(SQLAlchemyEnum(UserType), nullable=False, default=UserType.user)
    birthdate: date = db.Column(db.Date, nullable=True, default=None)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

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

    #region VALIDATION
    # PRIVATE_USER_ID
    @validates("private_user_id")
    def validate_private_user_id(self, key, private_user_id: str) -> str:
        if not valid_private_user_id(private_user_id):
            raise ValueError("Invalid user private identifier.")
        return private_user_id
    
    # PUBLIC_USER_ID
    @validates("public_user_id")
    def validate_public_user_id(self, key, public_user_id: str) -> str:
        if not valid_public_user_id(public_user_id):
            raise ValueError("Invalid user public identifier.")
        return public_user_id

    # USERNAME
    @validates("username")
    def validate_username(self, key, username: str) -> str:
        if not valid_string(username, length=(USER_USERNAME_LENGTH_MIN , USER_USERNAME_LENGTH_MAX), allow_empty=False):
            raise ValueError("Invalid username.")
        return username
    
    # EMAIL
    @validates("email")
    def validate_email(self, key, email: str) -> str:
        if not valid_email(email):
            raise ValueError("Invalid email.")
        return email
    
    # FRIEND_CODE
    @validates("friend_code")
    def validate_friend_code(self, key, friend_code: str) -> str:
        if friend_code is not None and not valid_friend_code(friend_code):
            raise ValueError("Invalid friend code.")
        return friend_code
    
    # PASSWORD_HASH
    @validates("password_hash")
    def validate_password_hash(self, key, password_hash: str) -> str:
        if not valid_password_hash(password_hash):
            raise ValueError("Invalid password hash.")
        return password_hash
    
    # PROFILE_PICTURE_URL
    @validates("profile_picture_url")
    def validate_profile_picture_url(self, key, profile_picture_url: str) -> str:
        if not valid_string(profile_picture_url, length=(1, USER_PROFILE_PICTURE_URL_LENGTH), allow_empty=False):
            raise ValueError("Invalid profile picture URL.")
        return profile_picture_url
    
    # GENDER
    @validates("gender")
    def validate_gender(self, key, gender: str) -> str:
        if not valid_string(gender, length=(1, USER_GENDER_LENGTH), allow_empty=True):
            raise ValueError("Invalid gender.")
        return gender
        
    # COUNTRY
    @validates("country")
    def validate_country(self, key, country: str) -> str:
        if not valid_string(country, length=(1, USER_COUNTRY_LENGTH), allow_empty=True):
            raise ValueError("Invalid country.")
        return country
    
    # ORIENTATION
    @validates("orientation")
    def validate_orientation(self, key, orientation: str) -> str:
        if not valid_string(orientation, length=(1, USER_ORIENTATION_LENGTH), allow_empty=True):
            raise ValueError("Invalid orientation.")
        return orientation
    
    # BIOGRAPHY
    @validates("biography")
    def validate_biography(self, key, biography: str) -> str:
        if not valid_text(biography, limit=True, allow_empty=True, length=(1, USER_BIOGRAPHY_TEXT_LIMIT)):
            raise ValueError("Invalid biography.")
        return biography
    
    # BIRTHDATE
    @validates("birthdate")
    def validate_birthdate(self, key, birthdate: date) -> date:
        if not valid_datetime(birthdate, allow_future_dates=False):
            raise ValueError("Invalid birthdate.")
        return birthdate
    
    # USER_TYPE
    @validates("user_type")
    def validate_user_type(self, key, user_type: Union[UserType, str]) -> str:
        if not valid_enum_element(user_type, UserType):
            raise ValueError("Invalid user type.")
        return UserType(user_type).value
    
    # CREATED_AT
    @validates("created_at")
    def validate_created_at(self, key, created_at: datetime) -> datetime:
        if not valid_datetime(created_at):
            raise ValueError("Invalid created at datetime.")
        return created_at
    #endregion VALIDATION

    def __repr__(self):
        return f"<User {self.private_user_id}>"
    
    class DictKeys(Enum):
        """Defines keys for the dictionary representation of the Users model."""
        ID = "id"
        USERNAME = "username"
        EMAIL = "email"
        FRIEND_CODE = "friend_code"
        PROFILE_PICTURE = "profile_picture"
        GENDER = "gender"
        COUNTRY = "country"
        ORIENTATION = "orientation"
        BIOGRAPHY = "biography"
        USER_TYPE = "user_type"
        BIRTH_DATE = "birth_date"
        CREATED_AT = "created_at"
        STATS = "stats"
        ACTIVE_ACCESSORIES = "active_accessories"


    def to_dict(self, exclude_fields: list[DictKeys] = []):
        """Converts the Users instance into a dictionary representation.

        This method converts the Users instance into a dictionary representation,
        allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the Users instance.
        """
        from app.models import UserStats, UserProfileAccessories

        upa_dict_keys = UserProfileAccessories.DictKeys

        user_stats: Union[UserStats, dict] = self.stats if isinstance(self.stats, UserStats) else {}

        data = {
            "id": self.public_user_id,
            "username": self.username,
            "email": self.email,
            "friend_code": self.friend_code,
            "profile_picture": self.profile_picture_url,
            "gender": self.gender,
            "country": self.country,
            "orientation": self.orientation,
            "biography": self.biography,
            "user_type": self.user_type.value,
            "birth_date": self.birthdate,
            "created_at": self.created_at,
            "stats": user_stats.to_dict() if isinstance(user_stats, UserStats) else {},
            "active_accessories": self.active_profile_accessories.to_dict(exclude_fields=[upa_dict_keys.USER_ID])
        }

        for field in exclude_fields:
            data.pop(field.value, None)
        
        return data
