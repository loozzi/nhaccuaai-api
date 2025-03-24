from src.models import Genre
from src.services import GenreService


class GenreController:
    def __init__(self):
        self.srv = GenreService()

    def get_all(self, limit: int, page: int, keyword: str) -> list:
        """
        Get all genres
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :return: The genres
        """
        offset = (page - 1) * limit
        # TODO: Handle return pagination form
        return self.srv.get_all(limit, offset, keyword)

    def get_by_id(self, id: int) -> Genre:
        """
        Get a genre by ID
        :param id: The genre ID
        :return: The genre
        """
        # TODO: Query list artists of genre
        return self.srv.get_by_id(id)

    def store(self, data: dict) -> Genre:
        """
        Store a new genre
        :param data: The genre data
        :return: The stored genre
        """
        return self.srv.store(data)

    def update(self):
        pass

    def destroy(self):
        pass
