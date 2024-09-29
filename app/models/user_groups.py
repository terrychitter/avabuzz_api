import datetime
from app import db

class UserGroups(db.Model): # type: ignore
    __tablename__ = "user_groups"

    private_group_id = db.Column(db.Integer, primary_key=True)
    public_group_id = db.Column(db.String(10), nullable=False, unique=True)
    group_name = db.Column(db.String(20), nullable=False)
    group_description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    owner_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)

    # Define the relationship to the Users model
    owner = db.relationship("Users", back_populates="groups")

    # Define the relationship to the Posts model
    posts = db.relationship("Posts", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserGroup {self.private_group_id}>"
    
    def to_dict(self):
        return {
            "public_id": self.public_group_id,
            "private_id": self.private_group_id,
            "owner": self.owner.to_dict(),
            "created_at": self.created_at,
            "name": self.group_name,
            "description": self.group_description
        }