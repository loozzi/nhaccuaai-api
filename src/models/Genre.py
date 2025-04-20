from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.Base import Base


class Genre(Base):
    __tablename__ = "genres"
    name: Mapped[str] = mapped_column(String, nullable=False)
    permalink: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, name: str, permalink: str) -> "Genre":
        self.name = name
        self.permalink = permalink
        self.save()
        return self

    def __repr__(self):
        return f"<Genre {self.id}>"
