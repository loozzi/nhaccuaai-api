from src.models import Genre
from src.services import ArtistService, GenreService
from src.utils.pagination import pagination_response


class GenreController:
    def __init__(self):
        self.srv = GenreService()
        self.artist_srv: ArtistService = ArtistService()

    def get_all(self, limit: int, page: int, keyword: str) -> list:
        """
        Get all genres
        :param limit: The limit
        :param page: The page
        :param keyword: The keyword
        :return: The genres
        """
        offset = (page - 1) * limit

        genres = self.srv.get_all(limit, offset, keyword)

        total = self.srv.count(keyword)

        return pagination_response(genres, limit, page, total)

    def get_by_id(self, id: int) -> Genre:
        """
        Get a genre by ID
        :param id: The genre ID
        :return: The genre
        """
        genre = self.srv.get_by_id(id)
        artists = self.artist_srv.get_by_genre_id(id) or []
        genre["artists"] = artists
        return genre

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
