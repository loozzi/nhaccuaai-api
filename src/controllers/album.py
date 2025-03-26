import datetime

from src.services.album import AlbumService


class AlbumController:
    def __init__(self):
        self.album_service: AlbumService = AlbumService()

    def get_all(self, limit: int, offset: int, keyword: str) -> list:
        """
        Get all albums
        :param limit: The limit
        :param offset: The offset
        :param keyword: The keyword
        :return: The albums
        """
        return self.album_service.get_all(limit, offset, keyword)

    def get_by_id(self, id: int) -> dict:
        """
        Get an album by ID
        :param id: The album ID
        :return: The album
        """
        return self.album_service.get_by_id(id)

    def store(self, data: dict) -> dict:
        """
        Store a new album
        :param data: The album data
        :return: The stored album
        """
        name = data.get("name")
        image = data.get("image")
        permalink = data.get("permalink")
        album_type = data.get("album_type")
        release_date = data.get("release_date")
        artist_ids = data.get("artist_ids")
        if not name or not permalink or not artist_ids:
            raise ValueError("Missing required fields")

        if release_date:
            release_date = release_date.split(" ")[0]
            release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d")

        payload = {
            "name": name,
            "image": image,
            "permalink": permalink,
            "album_type": album_type,
            "release_date": release_date,
            "artist_ids": artist_ids,
        }
        return self.album_service.store(payload)

    def update(self, id: int, data: dict) -> dict:
        """
        Update an album
        :param id: The album ID
        :param data: The album data
        :return: The updated album
        """

        name = data.get("name")
        image = data.get("image")
        permalink = data.get("permalink")
        album_type = data.get("album_type")
        release_date = data.get("release_date")
        artist_ids = data.get("artist_ids")
        if release_date:
            release_date = release_date.split(" ")[0]
            release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
        payload = {
            "name": name,
            "image": image,
            "permalink": permalink,
            "album_type": album_type,
            "release_date": release_date,
            "artist_ids": artist_ids,
        }
        return self.album_service.update(id, payload)

    def delete(self, id: int) -> dict:
        """
        Delete an album
        :param id: The album ID
        :return: The deleted album
        """
        return self.album_service.delete(id)
