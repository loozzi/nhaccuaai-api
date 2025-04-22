from src.models import Artist, Track, TrackArtist
from src.utils.enums import TrackType
from sqlalchemy.orm import Session


class TrackService:
    def __init__(self):
        pass

    def get_all(self, limit: int, offset: int, keyword: str, db=None) -> list:
        """
        Get all tracks
        :param limit: The limit
        :param offset: The offset
        :param keyword: The keyword
        :param db: Database session
        :return: The tracks
        """
        if not db:
            tracks = (
                Track.query.filter(Track.name.ilike("%{keyword}%".format(keyword=keyword)))
                .offset(offset=offset)
                .limit(limit)
                .all()
            )
        else:
            tracks = (
                db.query(Track)
                .filter(Track.name.ilike("%{keyword}%".format(keyword=keyword)))
                .offset(offset)
                .limit(limit)
                .all()
            )

        return [track.to_dict() for track in tracks]

    def get_by_permalink(self, permalink: str, db=None) -> Track:
        """
        Get a track by permalink
        :param permalink: The track permalink
        :param db: Database session
        :return: The track
        """
        if not db:
            track = Track.query.filter_by(permalink=permalink).first()
        else:
            track = db.query(Track).filter_by(permalink=permalink).first()
            
        if not track:
            raise ValueError("Track not found")
        return track.to_dict()

    def get_by_id(self, id: int, db=None) -> Track:
        """
        Get a track by ID
        :param id: The track ID
        :param db: Database session
        :return: The track
        """
        if not db:
            track = Track.query.get(id)
        else:
            track = db.query(Track).filter(Track.id == id).first()
            
        if not track:
            raise ValueError("Track not found")
        return track.to_dict()

    def store(self, data: dict, db=None) -> Track:
        """
        Store a new track
        :param data: The track data
        :param db: Database session
        :return: The stored track
        """
        album_id = data.get("album_id")
        name = data.get("name")
        file_url = data.get("file_url")
        duration = data.get("duration")
        permalink = data.get("permalink")
        type = data.get("type", TrackType.OTHER.value)
        release_date = data.get("release_date")
        track_number = data.get("track_number")
        image = data.get("image")

        track = Track(
            album_id,
            name,
            file_url,
            duration,
            permalink,
            type,
            release_date,
            track_number,
            image,
        )
        
        if db:
            track = track.save(db)
        else:
            track = track.save()
            
        return track.to_dict()

    def store_artist(self, track_id: int, artist_id: int, db=None) -> TrackArtist:
        """
        Store a new track artist
        :param track_id: The track ID
        :param artist_id: The artist ID
        :param db: Database session
        :return: The stored track artist
        """
        if not db:
            if not Track.query.get(track_id):
                raise ValueError("Track not found")
            if not Artist.query.get(artist_id):
                raise ValueError("Artist not found")
        else:
            if not db.query(Track).filter(Track.id == track_id).first():
                raise ValueError("Track not found")
            if not db.query(Artist).filter(Artist.id == artist_id).first():
                raise ValueError("Artist not found")

        track_artist = TrackArtist(track_id, artist_id)
        
        if db:
            track_artist = track_artist.save(db)
        else:
            track_artist = track_artist.save()
            
        return track_artist.to_dict()

    def update(self, id: int, data: dict, db=None) -> Track:
        """
        Update a track
        :param id: The track ID
        :param data: The track data
        :param db: Database session
        :return: The updated track
        """
        if not db:
            track = Track.query.get(id)
        else:
            track = db.query(Track).filter(Track.id == id).first()
            
        if not track:
            raise ValueError("Track not found")

        if db:
            track = track.update(db, **data)
        else:
            track = track.update(**data)
            
        return track.to_dict()

    def update_artists(self, id: int, artists: list, db=None) -> TrackArtist:
        """
        Update a track artist
        :param id: The track artist ID
        :param artists: The list of artists id
        :param db: Database session
        :return: The updated track artist
        """
        if not db:
            track = Track.query.get(id)
            current_artists = [artist.id for artist in track.artists]
        else:
            track = db.query(Track).filter(Track.id == id).first()
            track_artists = db.query(TrackArtist).filter(TrackArtist.track_id == id).all()
            current_artists = [ta.artist_id for ta in track_artists]
            
        if not track:
            raise ValueError("Track not found")

        for artist_id in artists:
            if artist_id not in current_artists:
                self.store_artist(id, artist_id, db)
        
        for artist_id in current_artists:
            if artist_id not in artists:
                if not db:
                    TrackArtist.query.filter_by(track_id=id, artist_id=artist_id).delete()
                else:
                    ta = db.query(TrackArtist).filter_by(track_id=id, artist_id=artist_id).first()
                    if ta:
                        ta.delete(db)

        return None

    def destroy(self, id: int, db=None) -> None:
        """
        Destroy a track
        :param id: The track ID
        :param db: Database session
        """
        if not db:
            track = Track.query.get(id)
            track_artists = TrackArtist.query.filter_by(track_id=id).all()
        else:
            track = db.query(Track).filter(Track.id == id).first()
            track_artists = db.query(TrackArtist).filter_by(track_id=id).all()
            
        if not track:
            raise ValueError("Track not found")
            
        for track_artist in track_artists:
            if db:
                track_artist.delete(db)
            else:
                track_artist.delete()
                
        if db:
            track.delete(db)
        else:
            track.delete()
            
        return None
