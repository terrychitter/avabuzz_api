from app import db

class HashTags(db.Model):
    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashtag_name = db.Column(db.String(50), nullable=False)
    views = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<HashTag {self.hashtag_id}>"
    
    def as_dict(self):
        return {
            "id": self.hashtag_id,
            "name": self.hashtag_name,
            "views": self.views,
            "post_count": self.post_count
        }