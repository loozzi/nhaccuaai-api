import datetime

from sqlalchemy import TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class Album(Base):
    __tablename__ = "albums"
    name: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(1023))
    permalink: Mapped[str] = mapped_column(String(255))
    album_type: Mapped[str] = mapped_column(String(255))
    release_date: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
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
        self.save()
        return self
