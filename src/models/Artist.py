from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .Base import BaseModel


class Artist(BaseModel):
    __tablename__ = "artists"

    name = Column(String(255), nullable=False)
    image = Column(String(1024), nullable=True)
    permalink = Column(String(255), nullable=False)
    albums = relationship("AlbumArtist", back_populates="artist")
    tracks = relationship("TrackArtist", back_populates="artist")

    def __init__(self, name: str, image: str, permalink: str):
        self.name = name
        self.image = image
        self.permalink = permalink

    def __repr__(self):
        return f"<Artist {self.name}>"
