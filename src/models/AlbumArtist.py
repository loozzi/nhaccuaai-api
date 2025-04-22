from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .Base import BaseModel


class AlbumArtist(BaseModel):
    __tablename__ = "album_artists"
    album_id = Column(Integer, ForeignKey("albums.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)

    album = relationship("Album", back_populates="artists")
    artist = relationship("Artist", back_populates="albums")

    def __init__(self, album_id: int, artist_id: int):
        self.album_id = album_id
        self.artist_id = artist_id
