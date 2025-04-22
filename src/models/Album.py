import datetime

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.orm import relationship

from .Base import BaseModel


class Album(BaseModel):
    __tablename__ = "albums"
    name = Column(String(255))
    image = Column(String(1023))
    permalink = Column(String(255))
    album_type = Column(String(255))
    release_date = Column(TIMESTAMP)
    artists = relationship("AlbumArtist", back_populates="album")
    tracks = relationship("Track", back_populates="album")

    def __init__(
        self,
        name: str,
        image: str,
        permalink: str,
        album_type: str,
        release_date: datetime.datetime,
    ):
        self.name = name
        self.image = image
        self.permalink = permalink
        self.album_type = album_type
        self.release_date = release_date
