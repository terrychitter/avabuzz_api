from enum import Enum

#region ------------------- PROFILE ACCESSORIES ------------------- #
class ProfileAccessoryType(Enum):
    """Defines the types of profile accessories available.

    This enum class defines the
    types of profile accessories that can be used on user/group profiles.

    Attributes:
        USER_BANNER (str): A banner that appears at the top of a user's profile.
        PROFILE_PICTURE_BORDER (str): A border that appears around a user's profile picture.
        BADGE (str): A badge that appears on a user's profile.
        GROUP_BANNER (str): A banner that appears at the top of a group's profile.
    
    Returns:
        None
    """
    USER_BANNER = "USER_BANNER"
    PROFILE_PICTURE_BORDER = "PROFILE-PICTURE_BORDER"
    BADGE = "BADGE"
    GROUP_BANNER = "GROUP_BANNER"

class ProfileType(Enum):
    """Defines the types of profiles available.

    This enum class defines the
    types of profiles that can be used with profile accessories.

    Attributes:
        USER_PROFILE (str): A profile associated with a user.
        GROUP_PROFILE (str): A profile associated with a group.

    Returns:
        None
    """
    USER_PROFILE = "USER_PROFILE"
    GROUP_PROFILE = "GROUP_PROFILE"

class OwnershipType(Enum):
    """Defines the types of ownership available.

    This enum class defines the
    types of ownership that can be associated with a profile accessory.

    Attributes:
        USER (str): Indicates that the accessory is owned by a user.
        GROUP (str): Indicates that the accessory is owned by a group.

    Returns:
        None
    """
    USER = "USER"
    GROUP = "GROUP"
#endregion ------------------- PROFILE ACCESSORIES ------------------- #


#region ---------------------- USERS --------------------------------- #
class UserType(Enum):
    """Enumeration of user types for the Users model.

    This enumeration defines the different types of users that can be created
    in the system, including regular users, administrators, and moderators.

    Attributes:
        USER (str): A regular user with limited permissions.
        ADMIN (str): An administrator with full permissions.
        MODERATOR (str): A moderator with limited permissions.

    Returns:
        None
    """
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
#endregion ------------------- USERS --------------------------------- #


#region ---------------------- POSTS ----------------------------------- #
class PostType(Enum):
    """Enumeration of post types for the Posts model.

    This enumeration defines the different types of posts that can be created
    by users, including text posts, image posts, video posts, and event posts.

    Attributes:
        POST (str): A text-based post with no media content.
        IMAGE (str): A post containing an image or photo.
        VIDEO (str): A post containing a video.
        EVENT (str): A post indicating an event or activity.
    
    Returns:
        None
    """
    POST = "POST"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    EVENT = "EVENT"
#endregion ------------------- POSTS --------------------------------- #

#region ---------------------- POST COMMENTS ------------------------- #
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
#endregion ------------------ POST COMMENTS ------------------------- #
