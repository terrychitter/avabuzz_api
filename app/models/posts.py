import datetime
from app import db
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class PostCategories(db.Model):
    __tablename__ = "post_categories"

    post_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_category_name = db.Column(db.String(50), nullable=False)
    post_category_description = db.Column(db.Text, nullable=True)

    # Define the relationship to the Posts model
    posts = db.relationship("Posts", back_populates="post_category")

    def __repr__(self):
        return f"<PostCategory {self.post_category_id}>"
    
    def as_dict(self):
        return {
            "id": self.post_category_id,
            "name": self.post_category_name,
            "description": self.post_category_description
        }

class PostHashTags(db.Model):
    __tablename__ = "post_hashtags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey("hashtags.hashtag_id"), primary_key=True)

    # Define relationship to HashTags model
    hashtag = db.relationship("HashTags", backref="post_hashtag")

    def __repr__(self):
        return f"<PostHashTag {self.post_id}-{self.hashtag_id}>"
    
    def as_dict(self):
        return {
            "post_id": self.post_id,
            "hashtag_id": self.hashtag_id
        }

class PostMedia(db.Model):
    __tablename__ = "post_media"

    post_media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    media_size_bytes = db.Column(db.Integer, nullable=False)
    media_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="media")

    def __repr__(self):
        return f"<PostMedia {self.post_media_id}>"
    
    def as_dict(self):
        return {
            "url": self.media_url,
            "order": self.media_order,
            "size_bytes": self.media_size_bytes,
        }

class PostReactionTypes(db.Model):
    __tablename__ = "post_reaction_types"

    post_reaction_type = db.Column(db.String(20), primary_key=True)

    def __repr__(self):
        return f"<PostReactionType {self.post_reaction_type}>"
    
    def to_dict(self):
        return {
            "type": self.post_reaction_type
        }

class PostReactionCounts(db.Model):
    __tablename__ = "post_reaction_counts"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), primary_key=True)
    post_reaction_type = db.Column(db.String(20), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)
    reaction_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<PostReactionCount {self.post_id}-{self.post_reaction_type}>"
    
    def as_dict(self, exclude_fields: list = []):
        data = {
            "post_id": self.post_id,
            "type": self.post_reaction_type,
            "count": self.reaction_count
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data
    
class PostReactions(db.Model):
    __tablename__ = "post_reactions"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True)
    post_reaction_type = db.Column(db.String(20), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="post_reactions")

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="post_reactions")

    def __repr__(self):
        return f"<PostReaction {self.post_id}-{self.user_id}-{self.post_reaction_type}>"
    
    def as_dict(self, exclude_fields: list = []):
        data = {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "reaction": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data

class Posts(db.Model):
    __tablename__ = "posts"

    class PostType(Enum):
        post = "post"
        image = "image"
        video = "video"
        event= "event"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_caption = db.Column(db.Text, nullable=True)
    post_type = db.Column(SQLAlchemyEnum(PostType), nullable=False)
    post_category_id = db.Column(db.Integer, db.ForeignKey("post_categories.post_category_id"), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=True)
    group_id = db.Column(db.String(10), db.ForeignKey("user_groups.private_group_id"), nullable=True)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Define relationship to PostCategories model
    post_category = db.relationship("PostCategories", back_populates="posts")

    # Define relationship to PostHashTags model with cascade
    post_hashtags = db.relationship("PostHashTags", backref="post", cascade="all, delete-orphan")

    # Define relationship to Hashtags model
    hashtags = db.relationship("HashTags", secondary="post_hashtags", back_populates="posts")

    # Define relationship to PostMedia model
    media = db.relationship("PostMedia", back_populates="post", cascade="all, delete-orphan")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="posts")

    # Define relationship to UserGroups model
    group = db.relationship("UserGroups", back_populates="posts")

    # Define relationship to PostReactionCounts model
    reactions = db.relationship("PostReactionCounts", backref="post", cascade="all, delete-orphan")

    # Define relationship to PostReactionTypes model
    post_reactions = db.relationship("PostReactions", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post {self.post_id}>"
    
    def to_dict(self, user_id=None, exclude_fields: list = ["user_reacted"]):
        data = {
            "id": self.post_id,
            "caption": self.post_caption,
            "type": self.post_type.value,
            "category": self.post_category.as_dict(),
            "view_count": self.view_count,
            "poster": self.user.as_dict(),
            "created_at": self.created_at,
            "hashtags": [tag.hashtag.as_dict()["hashtag_name"] for tag in self.post_hashtags],
            "media": [media.as_dict() for media in self.media],
            "reactions": [reaction.as_dict(exclude_fields=["post_id"]) for reaction in self.reactions],
        }
        
        # Check if user_id is provided, to fetch their reaction
        if user_id:
            user_reaction = next((reaction for reaction in self.post_reactions if reaction.user_id == user_id), None)
            data["user_reacted"] = bool(user_reaction)  # True if user has reacted, False otherwise
            data["user_reaction_type"] = user_reaction.post_reaction_type if user_reaction else None

        # Remove excluded fields from the dictionary
        for field in exclude_fields:
            data.pop(field, None)
        
        return data
