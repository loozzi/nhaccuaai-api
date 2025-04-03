from src.services import ArtistService, Crawler, TrackService


class TrackController:
    def __init__(self):
        self.srv = TrackService()
        self.crawler = Crawler()
        self.artist_srv = ArtistService()

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
        return self.crawler.song_info(id=link)
