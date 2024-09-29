import datetime
from app import db
from app.utils.id_generation import generate_uuid

class UserFollowers(db.Model):
    __tablename__ = "user_followers"

    follow_id = db.Column(db.Integer, primary_key=True, default=generate_uuid)
    follower_user_id = db.Column(db.Integer, db.ForeignKey("users.private_user_id"), nullable=False)
    followee_user_id = db.Column(db.Integer, db.ForeignKey("users.private_user_id"), nullable=False)
    followed_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Relationships
    follower = db.relationship("Users", foreign_keys=[follower_user_id])
    followee = db.relationship("Users", foreign_keys=[followee_user_id])

    def __repr__(self):
        return f"<UserFollowers {self.id}>"
    
    def to_dict(self,exclude_fields: list= []):
        data = {
            "follow_id": self.follow_id,
            "follower": self.follower.as_dict(),
            "followee": self.followee.as_dict(),
            "followed_at": self.followed_at
        }
    
        for field in exclude_fields:
            data.pop(field, None)
    
        return data