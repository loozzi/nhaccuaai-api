from src.models import Artist, Track, TrackArtist
from src.utils.enums import TrackType


class TrackService:
    def __init__(self):
        pass

    def get_artists(self, track_id: int) -> list:
        """
        Get all artists of a track
        :param track_id: The track ID
        :return: The artists
        """
        artists = TrackArtist.query.filter_by(track_id=track_id).all()
        if not artists:
            return None
        return [Artist.query.get(artist.artist_id) for artist in artists]

    def count(self, keyword: str) -> int:
        """
        Count all tracks
        :param keyword: The keyword
        :return: The count of tracks
        """
        count = Track.query.filter(
            Track.name.ilike("%{keyword}%".format(keyword=keyword))
        ).count()
        return count

    def get_all(self, limit: int, offset: int, keyword: str) -> list:
        """
        Get all tracks
        :param limit: The limit
        :param offset: The offset
        :param keyword: The keyword
        :return: The tracks
        """
        tracks = (
            Track.query.filter(Track.name.ilike("%{keyword}%".format(keyword=keyword)))
            .offset(offset=offset)
            .limit(limit)
            .all()
        )

        return [track.__str__() for track in tracks]

    def get_by_permalink(self, permalink: str) -> Track:
        """
        Get a track by permalink
        :param permalink: The track permalink
        :return: The track
        """
        track = Track.query.filter_by(permalink=permalink).first()
        if not track:
            raise ValueError("Track not found")
        return track.__str__()

    def get_by_id(self, id: int) -> Track:
        """
        Get a track by ID
        :param id: The track ID
        :return: The track
        """
        track = Track.query.get(id)
        if not track:
            raise ValueError("Track not found")

        track_artists = TrackArtist.query.filter_by(track_id=id).all()
        if track_artists:
            track.artists = self.get_artists(track_artists)
        return track.__str__()

    def store(self, data: dict) -> Track:
        """
        Store a new track
        :param data: The track data
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
        return track.__str__()

    def store_artist(self, track_id: int, artist_id: int) -> TrackArtist:
        """
        Store a new track artist
        :param track_id: The track ID
        :param artist_id: The artist ID
        :return: The stored track artist
        """
        if not Track.query.get(track_id):
            raise ValueError("Track not found")
        if not Artist.query.get(artist_id):
            raise ValueError("Artist not found")

        track_artist = TrackArtist(track_id, artist_id)
        return track_artist.__str__()

    def update(self, id: int, data: dict) -> Track:
        """
        Update a track
        :param id: The track ID
        :param data: The track data
        :return: The updated track
        """
        track = Track.query.get(id)
        if not track:
            raise ValueError("Track not found")

        return track.update(**data).__str__()

    def update_artists(self, id: int, artists: list) -> TrackArtist:
        """
        Update a track artist
        :param id: The track artist ID
        :param artists: The list of artists id
        :return: The updated track artist
        """
        track = Track.query.get(id)
        if not track:
            raise ValueError("Track not found")

        current_artists = [artist.id for artist in track.artists]
        for artist_id in artists:
            if artist_id not in current_artists:
                self.store_artist(id, artist_id)
            else:
                TrackArtist.query.filter_by(track_id=id, artist_id=artist_id).delete()

        return None

    def destroy(self, id: int) -> None:
        """
        Destroy a track
        :param id: The track ID
        """
        track = Track.query.get(id)
        if not track:
            raise ValueError("Track not found")
        track_artists = TrackArtist.query.filter_by(track_id=id).all()
        for track_artist in track_artists:
            track_artist.delete()
        track.delete()
        return None

    def get_by_album_id(self, id: int) -> list:
        """
        Get all tracks by album ID
        :param id: The album ID
        :return: The tracks
        """
        tracks = Track.query.filter_by(album_id=id).all()
        return [track.__str__() for track in tracks]

    def get_by_artist_id(self, id: int) -> list:
        """
        Get all tracks by artist ID
        :param id: The artist ID
        :return: The tracks
        """
        tracks = Track.query.join(TrackArtist).filter(TrackArtist.artist_id == id).all()
        return [track.__str__() for track in tracks]
