from app import db


class ProfileAccessories(db.Model):
    __tablename__ = "profile_accessories"

    accessory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accessory_name = db.Column(db.String(50), nullable=False)
    accessory_description = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    profile_accessory_type = db.Column(db.String(50), nullable=False)
    profile_type = db.Column(db.String(20), nullable=False)
    ownership_type = db.Column(db.String(20), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    default_accessory = db.Column(db.Boolean, nullable=False)
    owner_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Define relationship to OwnedAccessories model
    owned_accessories = db.relationship(
        "OwnedAccessories", back_populates="profile_accessory"
    )
