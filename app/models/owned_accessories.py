from app import db
from app.models.profile_accessories import ProfileAccessories


class OwnedAccessories(db.Model):
    __tablename__ = "owned_accessories"

    owned_accessory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.String(10), db.ForeignKey("users.private_user_id"), nullable=True
    )
    created_at = db.Column(db.DateTime, nullable=False)
    accessory_id = db.Column(
        db.Integer, db.ForeignKey("profile_accessories.accessory_id"), nullable=False
    )

    # Define relationship to ProfileAccessories model
    profile_accessory = db.relationship(
        "ProfileAccessories", back_populates="owned_accessories"
    )

    # Define relationships to UserProfileAccessories model
    user_profile_accessories_banner = db.relationship(
        "UserProfileAccessories",
        foreign_keys="[UserProfileAccessories.active_banner_id]",
        back_populates="active_banner",
    )
    user_profile_accessories_border = db.relationship(
        "UserProfileAccessories",
        foreign_keys="[UserProfileAccessories.active_profile_picture_border_id]",
        back_populates="active_profile_picture_border",
    )
    user_profile_accessories_badge = db.relationship(
        "UserProfileAccessories",
        foreign_keys="[UserProfileAccessories.active_badge_id]",
        back_populates="active_badge",
    )
