import datetime
from app import db
from enum import Enum
from app.utils.id_generation import generate_uuid
from sqlalchemy import Enum as SQLAlchemyEnum

class PostCategories(db.Model): # type: ignore
    """Represents a record of post categories in the database.

    This model stores records of post categories, which are used to categorize
    and group user posts by topic. Each post category can have multiple posts.

    Attributes:
        post_category_id (str): The unique identifier for the post category, which serves as the primary key. Defaults to a generated UUID.
        post_category_name (str): The name of the post category. This cannot be null.
        post_category_description (str, optional): The description of the post category. This can be null.
    
    Relationships:
        posts (Posts): A relationship to the Posts model, indicating the posts associated with the category.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_categories"

    # COLUMNS
    post_category_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_category_name = db.Column(db.String(50), nullable=False)
    post_category_description = db.Column(db.Text, nullable=True)

    # Define the relationship to the Posts model
    posts = db.relationship("Posts", back_populates="post_category")

    # METHODS
    def __repr__(self):
        return f"<PostCategory {self.post_category_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """
        Converts the PostCategories instance into a dictionary representation.

        This method converts the PostCategories instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostCategories instance.
        """
        data = {
            "id": self.post_category_id,
            "name": self.post_category_name,
            "description": self.post_category_description
        }

        for field in exclude_fields:
            data.pop(field, None)

class PostHashTags(db.Model): # type: ignore
    """Represents a record of hashtags associated with user posts in the database.

    This model stores records of hashtags associated with user posts, which are
    used to categorize and group posts by topic. Each hashtag is associated with
    a specific post and can have multiple posts.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        hashtag_id (str): The unique identifier for the hashtag, linked to the `hashtags` table. This serves as part of the primary key.
    
    Relationships:
        hashtag (HashTags): A relationship to the HashTags model, indicating the hashtag associated with the post.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_hashtags"

    # COLUMNS
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), primary_key=True)
    hashtag_id = db.Column(db.String(36), db.ForeignKey("hashtags.hashtag_id"), primary_key=True)

    # Define relationship to HashTags model
    hashtag = db.relationship("HashTags", backref="post_hashtag")

    # METHODS
    def __repr__(self):
        return f"<PostHashTag {self.post_id}-{self.hashtag_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostHashTags instance into a dictionary representation.

        This method converts the PostHashTags instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostHashTags instance.
        """
        data = {
            "post_id": self.post_id,
            "hashtag_id": self.hashtag_id
        }

        for field in exclude_fields:
            data.pop(field, None)

        return data

class PostMedia(db.Model): # type: ignore
    """Represents a record of media content for user posts in the database.

    This model stores records of media content for user posts, which can be
    images, videos, or other multimedia files. Each media record is associated
    with a specific post and can have multiple media files.

    Attributes:
        post_media_id (str): The unique identifier for the media record, which serves as the primary key. Defaults to a generated UUID.
        post_id (str): The unique identifier for the post, linked to the `posts` table. This cannot be null.
        media_url (str): The URL of the media file. This cannot be null.
        media_size_bytes (int): The size of the media file in bytes. This cannot be null.
        media_order (int): The order of the media file in the post. This cannot be null.
        created_at (datetime): The timestamp when the media record was created. Defaults to the current time.
    
    Relationships:
        post (Posts): A relationship to the Posts model, indicating the post associated with the media.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_media"

    # COLUMNS
    post_media_id = db.Column(db.Integer, primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    media_size_bytes = db.Column(db.Integer, nullable=False)
    media_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="media")

    # METHODS
    def __repr__(self):
        return f"<PostMedia {self.post_media_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostMedia instance into a dictionary representation.

        This method converts the PostMedia instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostMedia instance.
        """
        data = {
            "url": self.media_url,
            "order": self.media_order,
            "size_bytes": self.media_size_bytes,
        }

        for field in exclude_fields:
            data.pop(field, None)

        return data

class PostReactionTypes(db.Model): # type: ignore
    """Represents a record of reaction types for user posts in the database.

    This model stores the different types of reactions that users can have on
    posts, such as likes, dislikes, etc. Each reaction type is associated with
    a specific post and user.

    Attributes:
        post_reaction_type (str): The unique identifier for the reaction type, which serves as the primary key.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_reaction_types"

    # COLUMNS
    post_reaction_type = db.Column(db.String(20), primary_key=True)

    # METHODS
    def __repr__(self):
        return f"<PostReactionType {self.post_reaction_type}>"
    
    def to_dict(self, exclude_fields: list = []):
        """
        Converts the PostReactionTypes instance into a dictionary representation.

        This method converts the PostReactionTypes instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostReactionTypes instance.
        """
        data = {
            "type": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data

class PostReactionCounts(db.Model): # type: ignore
    """Represents a record of reaction counts on user posts in the database.

    This model stores the total number of reactions on user posts, which is used
    to display the reaction count on the post. Each reaction count is associated
    with a specific post and reaction type.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        post_reaction_type (str): The type of reaction, linked to the `post_reaction_types` table. This serves as part of the primary key.
        reaction_count (int): The total number of reactions of the specified type on the post. Defaults to 0.

    Relationships:
        post (Posts): A relationship to the Posts model, indicating the post associated with the reaction count.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_reaction_counts"

    # COLUMNS
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), primary_key=True)
    post_reaction_type = db.Column(db.String(20), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)
    reaction_count = db.Column(db.Integer, nullable=False, default=0)

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="reactions")

    # METHODS
    def __repr__(self):
        return f"<PostReactionCount {self.post_id}-{self.post_reaction_type}>"

    def to_dict(self, exclude_fields: list = []):
        """Converts the PostReactionCounts instance into a dictionary representation.

        This method converts the PostReactionCounts instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the PostReactionCounts instance.
        """
        data = {
            "post_id": self.post.to_dict(),
            "type": self.post_reaction_type,
            "count": self.reaction_count
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data
    
class PostReactions(db.Model): # type: ignore
    """
    Represents a record of reactions on user posts in the database.
    
    This model stores records of reactions on user posts, indicating the users
    who reacted to a specific post. Each reaction is associated with a specific
    post and user, and can be of different types such as likes, dislikes, etc.

    Attributes:
        post_id (str): The unique identifier for the post, linked to the `posts` table. This serves as part of the primary key.
        user_id (str): The unique identifier for the user who reacted to the post, linked to the `users` table. This serves as part of the primary key.
        post_reaction_type (str): The type of reaction, linked to the `post_reaction_types` table. This serves as part of the primary key.

    Relationships:
        user (Users): A relationship to the Users model, indicating the user who reacted to the post.
        post (Posts): A relationship to the Posts model, indicating the post associated with the reaction.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_reactions"

    # COLUMNS
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), primary_key=True)
    post_reaction_type = db.Column(db.String(20), db.ForeignKey("post_reaction_types.post_reaction_type"), primary_key=True)

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="post_reactions")

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="post_reactions")

    # METHODS
    def __repr__(self):
        return f"<PostReaction {self.post_id}-{self.user_id}-{self.post_reaction_type}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostReactions instance into a dictionary representation.

        This method converts the PostReactions instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostReactions instance.
        """
        data = {
            "post_id": self.post.to_dict(),
            "user_id": self.user.to_dict(),
            "reaction": self.post_reaction_type
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data

class PostComments(db.Model): # type: ignore
    """
    Represents a record of comments on user posts in the database.

    This model stores records of comments on user posts, which can be parent
    comments or replies to existing comments. Each comment is associated with
    a specific post and user, and can have multiple likes.

    Attributes:
        post_comment_id (str): The unique identifier for the post comment, which serves as the primary key. Defaults to a generated UUID.
        post_id (str): The unique identifier for the post, linked to the `posts` table. This cannot be null.
        user_id (str): The unique identifier for the user who created the comment, linked to the `users` table. This cannot be null.
        post_comment_text (str): The text content of the comment. This cannot be null.
        post_comment_status (CommentStatus): The status of the comment, which is an enumeration of comment statuses. Defaults to NORMAL.
        parent_post_comment_id (int, optional): The unique identifier for the parent comment, if the comment is a reply. This can be null.
        created_at (datetime): The timestamp when the comment was created. Defaults to the current time.
    
    Relationships:
        post (Posts): A relationship to the Posts model, indicating the post associated with the comment.
        user (Users): A relationship to the Users model, indicating the user who created the comment.
        parent_comment (PostComments): A self-referential relationship to the PostComments model, indicating the parent comment for replies.
        replies (PostComments): A relationship to the PostComments model, indicating the replies to the comment.
        likes (PostCommentLikes): A relationship to the PostCommentLikes model, indicating the likes on the comment.
        like_count (PostCommentLikeCounts): A relationship to the PostCommentLikeCounts model, indicating the like count on the comment.
    """
    # TABLE NAME
    __tablename__ = "post_comments"

    class CommentStatus(Enum):
        """Enumeration of comment statuses for the PostComments model.

        This enumeration defines the different statuses that a comment can have,
        including normal comments, hidden comments, and flagged comments.

        Attributes:
            NORMAL (str): A normal comment that is visible to users.
            HIDDEN (str): A hidden comment that is not visible to users.
            FLAGGED (str): A flagged comment that requires moderation.
        
        Returns:
            None
        """
        NORMAL = "NORMAL"
        HIDDEN = "HIDDEN"
        FLAGGED = "FLAGGED"

    # COLUMNS
    post_comment_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.post_id"), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    post_comment_text = db.Column(db.Text, nullable=False)
    post_comment_status = db.Column(SQLAlchemyEnum(CommentStatus), nullable=False, default=CommentStatus.NORMAL)
    parent_post_comment_id = db.Column(db.Integer, db.ForeignKey("post_comments.post_comment_id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    # Define relationship to Posts model
    post = db.relationship("Posts", back_populates="comments")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="comments")

    # Define self-referential relationship for parent comments and replies
    parent_comment = db.relationship("PostComments", backref=db.backref("replies", cascade="all, delete-orphan"), remote_side=[post_comment_id])

    # Define relationship to PostCommentLikes model
    likes = db.relationship("PostCommentLikes", back_populates="comment", cascade="all, delete-orphan")

    # Define relationship to PostCommentLikeCounts model
    like_count = db.relationship("PostCommentLikeCounts", back_populates="comment", cascade="all, delete-orphan")

    # METHODS
    def __repr__(self):
        return f"<PostComment {self.post_comment_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostComments instance into a dictionary representation.

        This method converts the PostComments instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostComments instance.
        """
        like_count_relationship = getattr(self, "like_count", [])
        
        data = {
            "id": self.post_comment_id,
            "post": self.post.to_dict(),
            "user": self.user.to_dict(),
            "content": self.post_comment_text,
            "status": self.post_comment_status.value,
            "like_count": like_count_relationship[0].post_comment_like_count if like_count_relationship and len(like_count_relationship) > 0 else 0,
            "created_at": self.created_at,
            "replies": [reply.to_dict() for reply in self.replies] if "replies" not in exclude_fields else []
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data

class PostCommentLikes(db.Model): # type: ignore
    """Represents a record of likes on post comments in the database.

    This model stores records of likes on post comments, indicating the users
    who liked a specific comment. Each like is associated with a post comment
    and a user who liked the comment.

    Attributes:
        post_comment_like_id (str): The unique identifier for the post comment like, which serves as the primary key. Defaults to a generated UUID.
        post_comment_id (int): The unique identifier for the post comment, linked to the `post_comments` table. This cannot be null.
        user_id (str): The unique identifier for the user who liked the comment, linked to the `users` table. This cannot be null.
        created_at (datetime): The timestamp when the like was created. Defaults to the current time.

    Relationships:
        comment (PostComments): A relationship to the PostComments model, indicating the comment associated with the like.
        user (Users): A relationship to the Users model, indicating the user who liked the comment.
    
    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "post_comment_likes"

    # COLUMNS
    post_comment_like_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_comment_id = db.Column(db.Integer, db.ForeignKey("post_comments.post_comment_id"), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey("users.private_user_id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # Define relationship to PostComments model
    comment = db.relationship("PostComments", back_populates="likes")

    # Define relationship to Users model
    user = db.relationship("Users", back_populates="comment_likes")

    def __repr__(self):
        return f"<PostCommentLike {self.post_comment_like_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostCommentLikes instance into a dictionary representation.

        This method converts the PostCommentLikes instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.

        Returns:
            dict: A dictionary representation of the PostCommentLikes instance.
        """
        data = {
            "id": self.post_comment_like_id,
            "comment": self.comment.to_dict(),
            "user": self.user.to_dict(),
            "created_at": self.created_at
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data

class PostCommentLikeCounts(db.Model): # type: ignore
    """Represents a record of like counts for post comments in the database.

    This model stores the total number of likes on a post comment, which is used
    to display the like count on the comment. Each comment can have multiple likes.

    Attributes:
        post_comment_id (int): The unique identifier for the post comment, linked to the `post_comments` table. This serves as the primary key.
        post_comment_like_count (int): The total number of likes on the post comment. Defaults to 0.
    
    Relationships:
        comment (PostComments): A relationship to the PostComments model, indicating the comment associated with the like count.
    """
    # TABLE NAME
    __tablename__ = "post_comment_like_counts"

    # COLUMNS
    post_comment_id = db.Column(db.Integer, db.ForeignKey("post_comments.post_comment_id"), primary_key=True)
    post_comment_like_count = db.Column(db.Integer, nullable=False, default=0)

    # Define relationship to PostComments model
    comment = db.relationship("PostComments", back_populates="like_count")

    # METHODS
    def __repr__(self):
        return f"<PostCommentLikeCount {self.post_comment_id}>"
    
    def to_dict(self, exclude_fields: list = []):
        """Converts the PostCommentLikeCounts instance into a dictionary representation.

        This method converts the PostCommentLikeCounts instance into a dictionary
        representation, allowing for exclusion of specified fields.

        Args:
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the PostCommentLikeCounts instance.
        """
        data = {
            "comment": self.comment.to_dict(),
            "like_count": self.post_comment_like_count
        }

        for field in exclude_fields:
            data.pop(field, None)
        
        return data

class Posts(db.Model): # type: ignore
    """Represents a record of user posts in the database.

    This model stores records of user posts, which can be of different types
    such as text posts, image posts, video posts, or event posts. Each post
    is associated with a specific category and can contain multiple hashtags.

    Attributes:
        post_id (str): The unique identifier for the post, which serves as the primary key. Defaults to a generated UUID.
        post_caption (str, optional): The caption or text content of the post, which can be null.
        post_type (PostType): The type of the post, which is an enumeration of post types. This cannot be null.
        post_category_id (int): The unique identifier for the post category, linked to the `post_categories` table. This cannot be null.
        user_id (str, optional): The unique identifier for the user who created the post, linked to the `users` table. This can be null for group posts.
        group_id (str, optional): The unique identifier for the group to which the post belongs, linked to the `user_groups` table. This can be null for user posts.
        view_count (int): The number of views or interactions on the post. Defaults to 0.
        created_at (datetime): The timestamp when the post was created. Defaults to the current time.

    Relationships:
        post_category (PostCategories): A relationship to the PostCategories model, indicating the category of the post.
        post_hashtags (PostHashTags): A relationship to the PostHashTags model, indicating the hashtags associated with the post.
        hashtags (HashTags): A relationship to the HashTags model, indicating the hashtags associated with the post.
        media (PostMedia): A relationship to the PostMedia model, indicating the media content associated with the post.
        user (Users): A relationship to the Users model, indicating the user who created the post.
        group (UserGroups): A relationship to the UserGroups model, indicating the group to which the post belongs.
        reactions (PostReactionCounts): A relationship to the PostReactionCounts model, indicating the reaction counts on the post.
        post_reactions (PostReactions): A relationship to the PostReactions model, indicating the reactions on the post.
        comments (PostComments): A relationship to the PostComments model, indicating the comments on the post.

    Returns:
        None
    """
    # TABLE NAME
    __tablename__ = "posts"

    class PostType(Enum):
        """Enumeration of post types for the Posts model.

        This enumeration defines the different types of posts that can be created
        by users, including text posts, image posts, video posts, and event posts.

        Attributes:
            post (str): A text-based post with no media content.
            image (str): A post containing an image or photo.
            video (str): A post containing a video.
            event (str): A post indicating an event or activity.
        
        Returns:
            None
        """
        post = "post"
        image = "image"
        video = "video"
        event= "event"
    
    # COLUMNS
    post_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
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

    # Define relationship to PostComments model
    comments = db.relationship("PostComments", back_populates="post", cascade="all, delete-orphan")

    # METHODS
    def __repr__(self):
        return f"<Post {self.post_id}>"
    
    def to_dict(self, user_id=None, exclude_fields: list = ["user_reacted"]):
        """Converts the Posts instance into a dictionary representation.
        
        This method converts the Posts instance into a dictionary representation,
        allowing for exclusion of specified fields. It also includes additional
        information such as hashtags, media, and reactions.

        Args:
            user_id (str): The unique identifier for the user viewing the post. This is used to fetch the user's reaction.
            exclude_fields (list): A list of fields to exclude from the dictionary representation.
        
        Returns:
            dict: A dictionary representation of the Posts instance.
        """
        post_hashtags_relationship = getattr(self, "post_hashtags", [])
        media_relationship = getattr(self, "media", [])
        reactions_relationship = getattr(self, "reactions", [])
        post_reactions_relationship = getattr(self, "post_reactions", [])
        
        data = {
            "id": self.post_id,
            "caption": self.post_caption,
            "type": self.post_type.value,
            "category": self.post_category.to_dict(),
            "view_count": self.view_count,
            "poster": self.user.to_dict(),
            "created_at": self.created_at,
            "hashtags": [tag.hashtag.to_dict()["name"] for tag in post_hashtags_relationship],
            "media": [media.to_dict() for media in media_relationship],
            "reactions": [reaction.to_dict(exclude_fields=["post_id"]) for reaction in reactions_relationship],
        }
        
        # Check if user_id is provided, to fetch their reaction
        if user_id:
            user_reaction = next((reaction for reaction in post_reactions_relationship if reaction.user_id == user_id), None)
            data["user_reacted"] = bool(user_reaction)  # True if user has reacted, False otherwise
            data["user_reaction_type"] = user_reaction.post_reaction_type if user_reaction else None

        # Remove excluded fields from the dictionary
        for field in exclude_fields:
            data.pop(field, None)
        
        return data
