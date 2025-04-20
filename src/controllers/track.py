from src.services import ArtistService, Crawler, CrawlerService, TrackService
from src.utils.enums import TrackType


class TrackController:
    def __init__(self):
        self.srv = TrackService()
        self.crawler = Crawler()
        self.artist_srv = ArtistService()
        self.crawl_srv = CrawlerService()

    def get_all(self, limit: int, page: int, keyword: str) -> list:
        """
        Get all tracks
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :return: The tracks
        """
        offset = (page - 1) * limit
        return self.srv.get_all(limit, offset, keyword)

    def get_by_id(self, id: int) -> dict:
        """
        Get a track by ID
        :param id: The track ID
        :return: The track
        """
        return self.srv.get_by_id(id)

    def get_by_permalink(self, permalink: str) -> dict:
        """
        Get a track by permalink
        :param permalink: The track permalink
        :return: The track
        """
        return self.srv.get_by_permalink(permalink)

    def store(self, data: dict) -> dict:
        """
        Store a new track
        :param data: The track data"
        """
        if "release_date" in data:
            data["release_date"] = data["release_date"].strftime("%Y-%m-%d")

        artists = data.get("artists")
        if artists is None:
            raise ValueError("Artists is required")

        for artist_id in artists:
            if self.artist_srv.get_by_id(artist_id) is None:
                raise ValueError("Artist not found")

        del data["artists"]
        track = self.srv.store(data)

        for artist_id in artists:
            self.srv.store_artist(track["id"], artist_id)

        return self.srv.get_by_id(track["id"])

    def update(self, id: int, data: dict) -> dict:
        """
        Update a track
        :param id: The track ID
        :param data: The track data
        :return: The updated track
        """
        if "release_date" in data:
            data["release_date"] = data["release_date"].strftime("%Y-%m-%d")

        artists = data.get("artists")
        if artists is not None:
            for artist_id in artists:
                if self.artist_srv.get_by_id(artist_id) is None:
                    raise ValueError("Artist not found")
        del data["artists"]

        self.srv.update_artists(id, artists)

        return self.srv.update(id, data)

    def destroy(self, id: int) -> dict:
        """
        Destroy a track
        :param id: The track ID
        :return: The destroyed track
        """
        return self.srv.destroy(id)

    def crawl(self, link: str) -> dict:
        """
        Crawl the tracks
        :param link: The link
        :return: The crawled tracks
        """
        song_info = self.crawler.song_info(id=link)

        if song_info is None:
            raise ValueError("Song not found")

        list_artists = []
        for artist in song_info["artists"]:
            list_artists.append(artist)

        for artist in song_info["album"]["artists"]:
            list_artists.append(artist)

        list_genres = []
        for artist in list_artists:
            list_genres += artist["genres"]

        list_genres = list(set(list_genres))
        # Store the genres
        list_genre_ids = self.crawl_srv.store_genres(list_genres)

        # Store the artists
        for artist in list_artists:
            artist["genres"] = list_genre_ids
            artist["permalink"] = artist["id"]
            del artist["id"]
            self.crawl_srv.store_artist(artist)

        # Store the album
        album = song_info["album"]
        album["permalink"] = album["id"]
        del album["id"]
        album = self.crawl_srv.store_album(album)

        # Store the track
        song_info["permalink"] = song_info["id"]
        song_info["album_id"] = album["id"]
        del song_info["id"]
        return self.crawl_srv.store_track(song_info)


# (psycopg2.errors.InvalidTextRepresentation) invalid input value for enum tracktype: \"track\"\nLINE 1: ...32cb4acd9df050bc2e197', '5vNRhkKd0yEAg8suGBpjeY', 'track', '...\n                                                             ^\n\n[SQL: INSERT INTO tracks (album_id, name, file_url, duration, image, permalink, type, release_date, track_number, is_deleted) VALUES (%(album_id)s, %(name)s, %(file_url)s, %(duration)s, %(image)s, %(permalink)s, %(type)s, %(release_date)s, %(track_number)s, %(is_deleted)s) RETURNING tracks.id, tracks.created_at, tracks.updated_at]\n[parameters: {'album_id': 1, 'name': 'APT.', 'file_url': 'D:\\\\College\\\\VI\\\\Dự án\\\\code\\\\nhaccuaai-api\\\\songs\\\\APT. - ROSÉ.mp3', 'duration': 169917, 'image': 'https://i.scdn.co/image/ab67616d0000b27336032cb4acd9df050bc2e197', 'permalink': '5vNRhkKd0yEAg8suGBpjeY', 'type': 'track', 'release_date': '2024-10-18', 'track_number': 1, 'is_deleted': False}]
