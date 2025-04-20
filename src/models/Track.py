import datetime

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.enums import TrackType, track_type_enum

from .Base import Base


class Track(Base):
    __tablename__ = "tracks"
    album_id: Mapped[int] = mapped_column(Integer, ForeignKey("albums.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    file_url: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String)
    permalink: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Enum(TrackType), default=TrackType.OTHER.value)
    release_date: Mapped[datetime.date] = mapped_column(TIMESTAMP)
    track_number: Mapped[int] = mapped_column(Integer)

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
        self.save()
        return self
