from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class Artist(Base):
    __tablename__ = "artists"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(1024), nullable=True)
    permalink: Mapped[str] = mapped_column(String(255), nullable=False)
    albums = relationship("AlbumArtist", back_populates="artist")
    tracks = relationship("TrackArtist", back_populates="artist")

    def __init__(self, name: str, image: str, permalink: str) -> "Artist":
        self.name = name
        self.image = image
        self.permalink = permalink
        self.save()
        return self

    def __repr__(self):
        return f"<Artist {self.name}>"
