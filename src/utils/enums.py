from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    ARTIST = "artist"
    GUEST = "guest"


class TrackType(Enum):
    TRACK = "track"
    PODCAST = "podcast"
    EPISODE = "episode"
    LIVE = "live"
    REMIX = "remix"
    OTHER = "other"
