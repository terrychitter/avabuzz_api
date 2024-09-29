from app import db
from app.utils.id_generation import generate_uuid

class HashTags(db.Model): # type: ignore
    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    hashtag_name = db.Column(db.String(50), nullable=False)
    views = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)

    # Define the relationship between the HashTags and Posts models
    posts = db.relationship("Posts", secondary="post_hashtags", back_populates="hashtags")

    def __repr__(self):
        return f"<HashTag {self.hashtag_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        data = {
            "hashtag_id": self.hashtag_id,
            "hashtag_name": self.hashtag_name,
            "views": self.views,
            "post_count": self.post_count
        }
    
        for field in exclude_fields:
            data.pop(field, None)
    
        return data