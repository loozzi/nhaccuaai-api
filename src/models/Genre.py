from sqlalchemy import Column, String

from src.models.Base import BaseModel


class Genre(BaseModel):
    __tablename__ = "genres"
    name = Column(String, nullable=False)
    permalink = Column(String, nullable=False)

    def __init__(self, name: str, permalink: str):
        self.name = name
        self.permalink = permalink

    def __repr__(self):
        return f"<Genre {self.id}>"
