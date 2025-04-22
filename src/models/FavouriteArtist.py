from sqlalchemy import Column, ForeignKey, Integer

from .Base import BaseModel


class FavouriteArtist(BaseModel):
    __tablename__ = "favourite_artists"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)

    def __init__(self, user_id: int, artist_id: int):
        exists = (
            self.query.filter_by(user_id=user_id).filter_by(artist_id=artist_id).first()
        )
        if exists:
            exists.is_deleted = False
            exists.save()
            return exists
        self.user_id = user_id
        self.artist_id = artist_id

    def __repr__(self):
        return f"<FavouriteArtist {self.id}>"

    @classmethod
    def get_user_favourites(cls, user_id: int, db=None):
        """
        Get all favourite artists of a user
        :param user_id: The user ID
        :param db: Database session
        :return: The favourite artists
        """
        if db:
            return (
                db.query(cls)
                .filter(cls.is_deleted == False)
                .filter(cls.user_id == user_id)
                .all()
            )
        else:
            return cls.query.filter_by(is_deleted=False).filter_by(user_id=user_id).all()

    @classmethod
    def toggle(cls, user_id: int, artist_id: int, db=None):
        """
        Toggle a favourite artist
        :param user_id: The user ID
        :param artist_id: The artist ID
        :param db: Database session
        :return: The favourite artist
        """
        if db:
            favourite_artist = (
                db.query(cls)
                .filter(cls.user_id == user_id)
                .filter(cls.artist_id == artist_id)
                .first()
            )
        else:
            favourite_artist = (
                cls.query.filter_by(user_id=user_id).filter_by(artist_id=artist_id).first()
            )
            
        if favourite_artist:
            if favourite_artist.is_deleted:
                favourite_artist.is_deleted = False
            else:
                favourite_artist.is_deleted = True
                
            if db:
                favourite_artist.save(db)
            else:
                favourite_artist.save()
                
            return favourite_artist
        else:
            raise Exception("Favourite artist not found")

    @classmethod
    def delete_all(cls, artist_id: int, db=None):
        """
        Delete all favourite artists of an artist
        :param artist_id: The artist ID
        :param db: Database session
        """
        if db:
            favourite_artists = db.query(cls).filter(cls.artist_id == artist_id).all()
            for favourite_artist in favourite_artists:
                favourite_artist.delete(db)
        else:
            favourite_artists = cls.query.filter_by(artist_id=artist_id).all()
            for favourite_artist in favourite_artists:
                favourite_artist.delete()
                
        return None
