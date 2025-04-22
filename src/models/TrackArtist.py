from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .Base import BaseModel


class TrackArtist(BaseModel):
    __tablename__ = "track_artists"
    track_id = Column(Integer, ForeignKey("tracks.id"))
    artist_id = Column(Integer, ForeignKey("artists.id"))

    track = relationship("Track", back_populates="artists")
    artist = relationship("Artist", back_populates="tracks")

    def __init__(self, track_id: int, artist_id: int):
        self.track_id = track_id
        self.artist_id = artist_id
