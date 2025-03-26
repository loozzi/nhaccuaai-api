from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class TrackArtist(Base):
    __tablename__ = "track_artists"
    track_id: Mapped[int] = mapped_column(Integer, ForeignKey("tracks.id"))
    artist_id: Mapped[int] = mapped_column(Integer, ForeignKey("artists.id"))

    track = relationship("Track", back_populates="artists")
    artist = relationship("Artist", back_populates="tracks")

    def __init__(self, track_id: int, artist_id: int):
        self.track_id = track_id
        self.artist_id = artist_id
        self.save()
        return self
