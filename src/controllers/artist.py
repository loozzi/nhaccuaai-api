from src.services import ArtistService


class ArtistController:
    def __init__(self):
        self.srv = ArtistService()

    def get_all(self, limit: int, page: int, keyword: str) -> list:
        """
        Get all artists
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :return: The artists
        """
        offset = (page - 1) * limit
        return self.srv.get_all(limit, offset, keyword)

    def get_by_id(self, id: int) -> dict:
        """
        Get an artist by ID
        :param id: The artist ID
        :return: The artist
        """
        # TODO: Query list tracks & albums of artist
        return self.srv.get_by_id(id)

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
