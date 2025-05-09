from src.services import (
    AlbumService,
    ArtistService,
    Crawler,
    CrawlerService,
    TrackService,
)
from src.utils.pagination import pagination_response


class TrackController:
    def __init__(self):
        self.srv = TrackService()
        self.crawler = Crawler()
        self.artist_srv = ArtistService()
        self.track_srv = TrackService()
        self.album_srv = AlbumService()
        self.crawl_srv = CrawlerService()

    def get_all(self, limit: int, page: int, keyword: str) -> list:
        """
        Get all tracks
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :return: The tracks
        """
        # TODO: Query type of track, e.g: album, single, popular, etc. Default is newest
        offset = (page - 1) * limit
        tracks = self.srv.get_all(limit, offset, keyword)

        # tracks = list(map(lambda track: track.__str__(), tracks))
        tracks_response = [
            {
                "id": track["id"],
                "name": track["name"],
                "image": track["image"],
                "artists": self.track_srv.get_artists(track["id"]),
                "permalink": track["permalink"],
                "type": track["type"],
                "duration": track["duration"],
            }
            for track in tracks
        ]

        total = self.srv.count(keyword)

        return pagination_response(tracks_response, limit, page, total)

    def get_by_id(self, id: int) -> dict:
        """
        Get a track by ID
        :param id: The track ID
        :return: The track
        """
        track = self.srv.get_by_id(id)
        track["artists"] = self.track_srv.get_artists(id)

        try:
            album = self.album_srv.get_by_id(track["album_id"])
            track["album"] = album
            del track["album_id"]
        except ValueError:
            print("Album not found")
        return track

    def get_by_permalink(self, permalink: str) -> dict:
        """
        Get a track by permalink
        :param permalink: The track permalink
        :return: The track
        """
        track = self.srv.get_by_permalink(permalink)
        track["artists"] = self.track_srv.get_artists(track["id"])
        try:
            album = self.album_srv.get_by_id(track["album_id"])
            track["album"] = album
            del track["album_id"]
        except ValueError:
            print("Album not found")
        return track

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
        id = link.split("/")[-1].split("?")[0]
        song_info = self.crawler.song_info(id=id)

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
