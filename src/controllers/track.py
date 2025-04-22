from src.services import ArtistService, Crawler, CrawlerService, TrackService
from src.utils.enums import TrackType


class TrackController:
    def __init__(self):
        self.srv = TrackService()
        self.crawler = Crawler()
        self.artist_srv = ArtistService()
        self.crawl_srv = CrawlerService()

    def get_all(self, limit: int, page: int, keyword: str, db=None) -> list:
        """
        Get all tracks
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :param db: Database session
        :return: The tracks
        """
        offset = (page - 1) * limit
        return self.srv.get_all(limit, offset, keyword, db)

    def get_by_id(self, id: int, db=None) -> dict:
        """
        Get a track by ID
        :param id: The track ID
        :param db: Database session
        :return: The track
        """
        return self.srv.get_by_id(id, db)

    def get_by_permalink(self, permalink: str, db=None) -> dict:
        """
        Get a track by permalink
        :param permalink: The track permalink
        :param db: Database session
        :return: The track
        """
        return self.srv.get_by_permalink(permalink, db)

    def store(self, data: dict, db=None) -> dict:
        """
        Store a new track
        :param data: The track data
        :param db: Database session
        :return: The created track
        """
        if "release_date" in data:
            data["release_date"] = data["release_date"].strftime("%Y-%m-%d")

        artists = data.get("artists")
        if artists is None:
            raise ValueError("Artists is required")

        for artist_id in artists:
            if self.artist_srv.get_by_id(artist_id, db) is None:
                raise ValueError("Artist not found")

        del data["artists"]
        track = self.srv.store(data, db)

        for artist_id in artists:
            self.srv.store_artist(track["id"], artist_id, db)

        return self.srv.get_by_id(track["id"], db)

    def update(self, id: int, data: dict, db=None) -> dict:
        """
        Update a track
        :param id: The track ID
        :param data: The track data
        :param db: Database session
        :return: The updated track
        """
        if "release_date" in data and data["release_date"]:
            data["release_date"] = data["release_date"].strftime("%Y-%m-%d")

        artists = data.get("artists")
        if artists is not None:
            for artist_id in artists:
                if self.artist_srv.get_by_id(artist_id, db) is None:
                    raise ValueError("Artist not found")
            
            self.srv.update_artists(id, artists, db)
            del data["artists"]

        return self.srv.update(id, data, db)

    def destroy(self, id: int, db=None) -> dict:
        """
        Destroy a track
        :param id: The track ID
        :param db: Database session
        :return: The destroyed track
        """
        return self.srv.destroy(id, db)

    def crawl(self, link: str, db=None) -> dict:
        """
        Crawl the tracks
        :param link: The link
        :param db: Database session
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
        list_genre_ids = self.crawl_srv.store_genres(list_genres, db)

        # Store the artists
        for artist in list_artists:
            artist["genres"] = list_genre_ids
            artist["permalink"] = artist["id"]
            del artist["id"]
            self.crawl_srv.store_artist(artist, db)

        # Store the album
        album = song_info["album"]
        album["permalink"] = album["id"]
        del album["id"]
        album = self.crawl_srv.store_album(album, db)

        # Store the track
        song_info["permalink"] = song_info["id"]
        song_info["album_id"] = album["id"]
        del song_info["id"]
        return self.crawl_srv.store_track(song_info, db)
