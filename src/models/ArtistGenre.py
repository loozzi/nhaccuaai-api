from sqlalchemy import Column, ForeignKey, Integer

from .Base import BaseModel


class ArtistGenre(BaseModel):
    __tablename__ = "artist_genres"
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

    def __init__(self, artist_id: int, genre_id: int):
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

    def __repr__(self):
        return f"<ArtistGenre {self.id}>"

    @classmethod
    def get_artist_genres(cls, artist_id: int, db=None):
        """
        Get all genres of an artist
        :param artist_id: The artist ID
        :param db: Database session
        :return: The genres
        """
        if db:
            return (
                db.query(cls)
                .filter(cls.is_deleted == False)
                .filter(cls.artist_id == artist_id)
                .all()
            )
        else:
            return (
                cls.query.filter_by(is_deleted=False)
                .filter_by(artist_id=artist_id)
                .all()
            )

    @classmethod
    def get_genre_artists(cls, genre_id: int, db=None):
        """
        Get all artists of a genre
        :param genre_id: The genre ID
        :param db: Database session
        :return: The artists
        """
        if db:
            return (
                db.query(cls)
                .filter(cls.is_deleted == False)
                .filter(cls.genre_id == genre_id)
                .all()
            )
        else:
            return (
                cls.query.filter_by(is_deleted=False)
                .filter_by(genre_id=genre_id)
                .all()
            )

    @classmethod
    def delete_all(cls, artist_id: int, db=None):
        """
        Delete all artist genres
        :param artist_id: The artist ID
        :param db: Database session
        """
        if db:
            artist_genres = db.query(cls).filter(cls.artist_id == artist_id).all()
            for artist_genre in artist_genres:
                artist_genre.delete(db)
        else:
            artist_genres = cls.query.filter_by(artist_id=artist_id).all()
            for artist_genre in artist_genres:
                artist_genre.delete()
        return None
