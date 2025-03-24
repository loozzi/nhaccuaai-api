from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class AlbumArtist(Base):
    __tablename__ = "album_artists"
    album_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("albums.id"), primary_key=True
    )
    artist_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("artists.id"), primary_key=True
    )

    album = relationship("Album", back_populates="artists")
    artist = relationship("Artist", back_populates="albums")

    def __init__(self, album_id: int, artist_id: int):
        self.album_id = album_id
        self.artist_id = artist_id
        self.save()
        return self
