from app import db


class UserPrivateId(db.Model): # type: ignore
    """
    This class represents the user_private_ids table and is used to store private ids that have been generated.
    """
    __tablename__ = "user_private_ids"

    private_id = db.Column(db.String(10), primary_key=True)

