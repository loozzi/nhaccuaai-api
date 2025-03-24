from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class FavouriteArtist(Base):
    __tablename__ = "favourite_artists"
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    artist_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("artists.id"), primary_key=True
    )

    def __init__(self, user_id: int, artist_id: int) -> "FavouriteArtist":
        self.user_id = user_id
        self.artist_id = artist_id
        self.save()
        return self

    def __repr__(self):
        return f"<FavouriteArtist {self.id}>"

    def get_user_favourites(self, user_id: int) -> list:
        """
        Get all favourite artists of a user
        :param user_id: The user ID
        :return: The favourite artists
        """
        return self.query.filter_by(is_deleted=False).filter_by(user_id=user_id).all()

    def toggle(self, user_id: int, artist_id: int) -> "FavouriteArtist":
        """
        Toggle a favourite artist
        :param user_id: The user ID
        :param artist_id: The artist ID
        :return: The favourite artist
        """
        favourite_artist = (
            self.query.filter_by(user_id=user_id).filter_by(artist_id=artist_id).first()
        )
        if favourite_artist:
            if favourite_artist.is_deleted:
                favourite_artist.is_deleted = False
            else:
                favourite_artist.is_deleted = True
            favourite_artist.save()
            return favourite_artist
        else:
            raise Exception("Favourite artist not found")
