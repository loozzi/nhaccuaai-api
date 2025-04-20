from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class ArtistGenre(Base):
    __tablename__ = "artist_genres"
    artist_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("artists.id"), primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("genres.id"), primary_key=True
    )

    def __init__(self, artist_id: int, genre_id: int) -> "ArtistGenre":
        exists = (
            self.query.filter_by(artist_id=artist_id)
            .filter_by(genre_id=genre_id)
            .first()
        )
        if exists:
            exists.is_deleted = False
            exists.save()
            return exists

        self.artist_id = artist_id
        self.genre_id = genre_id
        self.save()
        return self

    def __repr__(self):
        return f"<ArtistGenre {self.id}>"

    @staticmethod
    def get_artist_genres(artist_id: int) -> list:
        """
        Get all genres of an artist
        :param artist_id: The artist ID
        :return: The genres
        """
        return (
            ArtistGenre.query.filter_by(is_deleted=False)
            .filter_by(artist_id=artist_id)
            .all()
        )

    @staticmethod
    def get_genre_artists(genre_id: int) -> list:
        """
        Get all artists of a genre
        :param genre_id: The genre ID
        :return: The artists
        """
        return (
            ArtistGenre.query.filter_by(is_deleted=False)
            .filter_by(genre_id=genre_id)
            .all()
        )

    @staticmethod
    def delete_all(artist_id: int) -> None:
        """
        Delete all artist genres
        :param artist_id: The artist ID
        """
        artist_genres = ArtistGenre.query.filter_by(artist_id=artist_id).all()
        for artist_genre in artist_genres:
            artist_genre.delete()
        return None
