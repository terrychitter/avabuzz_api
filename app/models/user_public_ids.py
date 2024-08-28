from app import db


class UserPublicId(db.Model):
    """
    This class represents the user_public_id_sequence table and is used to store public ids that have been generated.
    """
    __tablename__ = "user_public_ids"

    public_id = db.Column(db.String(10), primary_key=True)

