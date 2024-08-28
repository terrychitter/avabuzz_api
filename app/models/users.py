from app import db
from app.models.owned_accessories import OwnedAccessories
from app.models.profile_accessories import ProfileAccessories
from sqlalchemy.sql import func
from sqlalchemy import Enum
import enum


class UserProfileAccessories(db.Model):
    __tablename__ = "user_profile_accessories"

    user_id = db.Column(
        db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True
    )
    active_banner_id = db.Column(
        db.Integer,
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )
    active_profile_picture_border_id = db.Column(
        db.Integer,
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )
    active_badge_id = db.Column(
        db.Integer,
        db.ForeignKey("owned_accessories.owned_accessory_id"),
        nullable=False,
    )

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="active_profile_accessories")

    # Define relationships to OwnedAccessories model
    active_banner = db.relationship(
        "OwnedAccessories",
        foreign_keys=[active_banner_id],
        back_populates="user_profile_accessories_banner",
    )
    active_profile_picture_border = db.relationship(
        "OwnedAccessories",
        foreign_keys=[active_profile_picture_border_id],
        back_populates="user_profile_accessories_border",
    )
    active_badge = db.relationship(
        "OwnedAccessories",
        foreign_keys=[active_badge_id],
        back_populates="user_profile_accessories_badge",
    )


class UserStats(db.Model):
    __tablename__ = "user_stats"
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True)
    follower_count = db.Column(db.Integer, nullable=False)
    following_count = db.Column(db.Integer, nullable=False)
    post_count = db.Column(db.Integer, nullable=False)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="stats")

    def __repr__(self):
        return f"<UserStats {self.user_id}>"


class Users(db.Model):
    class UserType(enum.Enum):
        user = "user"
        admin = "admin"
        moderator = "moderator"

    __tablename__ = "users"
    private_user_id = db.Column(db.String(10), primary_key=True, nullable=False)
    public_user_id = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture_url = db.Column(db.String(255), nullable=True, default="https://placehold.co/400")
    gender = db.Column(db.String(20), nullable=True, default="None")
    country = db.Column(db.String(255), nullable=True, default="None")
    orientation = db.Column(db.String(20), nullable=True, default="None")
    biography = db.Column(db.Text, nullable=True)
    user_type = db.Column(db.Enum(UserType), nullable=False, default="user")
    birthdate = db.Column(db.Date, nullable=True, default=None)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Define relationship to UserStats model
    stats = db.relationship("UserStats", uselist=False, back_populates="user", cascade="all, delete-orphan")
    active_profile_accessories = db.relationship(
        "UserProfileAccessories", back_populates="user", uselist=False
    )

    def __repr__(self):
        return f"<User {self.private_user_id}>"

    def as_dict(self):
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

        return {
            "private_user_id": self.private_user_id,
            "public_user_id": self.public_user_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "profile_picture_url": self.profile_picture_url,
            "gender": self.gender,
            "country": self.country,
            "orientation": self.orientation,
            "biography": self.biography,
            "user_type": self.user_type.value,
            "birth_date": self.birthdate,
            "created_at": self.created_at,
            "active": self.active,
            "user_stats": {
                "follower_count": user_stats.follower_count if user_stats else None,
                "following_count": user_stats.following_count if user_stats else None,
                "post_count": user_stats.post_count if user_stats else None,
            },
            "active_accessories": {
                "active_banner_url": active_banner_url,
                "active_profile_picture_border_url": active_profile_picture_border_url,
                "active_badge_url": active_badge_url,
            },
        }
