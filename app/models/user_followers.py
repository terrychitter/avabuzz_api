import datetime
from app import db

class UserFollowers(db.Model):
    __tablename__ = "user_followers"

    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_user_id = db.Column(db.Integer, db.ForeignKey("users.private_user_id"), nullable=False)
    followee_user_id = db.Column(db.Integer, db.ForeignKey("users.private_user_id"), nullable=False)
    followed_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Relationships
    follower = db.relationship("Users", foreign_keys=[follower_user_id])
    followee = db.relationship("Users", foreign_keys=[followee_user_id])

    def __repr__(self):
        return f"<UserFollowers {self.id}>"
    
    def to_dict(self):
        return {
            "follow_id": self.follow_id,
            "follower": self.follower.to_dict(),
            "followee": self.followee.to_dict(),
            "followed_at": self.followed_at
        }