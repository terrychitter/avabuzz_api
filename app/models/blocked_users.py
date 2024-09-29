from app import db
from datetime import datetime
from app.utils.id_generation import generate_uuid

class BlockedUsers(db.Model): # type: ignore
    __tablename__ = "blocked_users"

    blocked_users_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    blocker_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    blocked_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    blocked_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Define the relationship between the BlockedUsers and Users models
    blocker = db.relationship("Users", foreign_keys=[blocker_id])
    blocked = db.relationship("Users", foreign_keys=[blocked_id])

    def __repr__(self):
        return f"<BlockedUsers {self.blocked_users_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        data = {
            "blocked_users_id": self.blocked_users_id,
            "blocker": self.blocker.to_dict(),
            "blocked_id": self.blocked.to_dict(),
            "blocked_at": self.blocked_at
        }
    
        for field in exclude_fields:
            data.pop(field, None)
    
        return data