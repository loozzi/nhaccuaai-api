import datetime

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.utils.enums import TrackType, track_type_enum
from .Base import BaseModel


class Track(BaseModel):
    __tablename__ = "tracks"
    album_id = Column(Integer, ForeignKey("albums.id"))
    name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    image = Column(String)
    permalink = Column(String, nullable=False)
    type = Column(Enum(TrackType), default=TrackType.OTHER.value)
    release_date = Column(TIMESTAMP)
    track_number = Column(Integer)

    album = relationship("Album", back_populates="tracks")
    artists = relationship("TrackArtist", back_populates="track")

    def __init__(
        self,
        album_id: int,
        name: str,
        file_url: str,
        duration: int,
        permalink: str,
        type: str = TrackType.OTHER.value,
        release_date: datetime.date = None,
        track_number: int = None,
        image: str = None,
    ):
        self.album_id = album_id
        self.name = name
        self.file_url = file_url
        self.duration = duration
        self.permalink = permalink
        self.type = track_type_enum[type]
        self.release_date = release_date
        self.track_number = track_number
        self.image = image
