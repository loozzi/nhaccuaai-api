from src.services import AlbumService, ArtistService, TrackService
from src.utils.pagination import pagination_response


class ArtistController:
    def __init__(self):
        self.srv = ArtistService()
        self.album_srv: AlbumService = AlbumService()
        self.track_srv: TrackService = TrackService()

    def get_all(self, limit: int, page: int, keyword: str) -> list:
        """
        Get all artists
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :return: The artists
        """
        offset = (page - 1) * limit
        artists = self.srv.get_all(limit, offset, keyword)
        total = self.srv.count(keyword)

        return pagination_response(artists, limit, page, total)

    def get_by_id(self, id: int) -> dict:
        """
        Get an artist by ID
        :param id: The artist ID
        :return: The artist
        """
        # TODO: Query list tracks & albums of artist
        artist = self.srv.get_by_id(id)
        albums = self.album_srv.get_albums_by_artist_id(id) or []
        tracks = self.track_srv.get_by_artist_id(id) or []

        artist["albums"] = albums
        artist["tracks"] = tracks
        return artist

    def store(self, data: dict) -> dict:
        """
        Store a new artist
        :param data: The artist data
        :return: The stored artist
        """
        return self.srv.store(data)

    def update(self, id: int, data: dict) -> dict:
        """
        Update an artist
        :param id: The artist ID
        :param data: The artist data
        :return: The updated artist
        """
        return self.srv.update(id, data)

    def destroy(self, id: int):
        """
        Destroy an artist
        :param id: The artist ID
        """
        return self.srv.destroy(id)
