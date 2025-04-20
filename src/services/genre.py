from src.models import Genre


class GenreService:
    def __init__(self):
        pass

    def get_all(self, limit: int, offset: int, keyword: str) -> list:
        """
        Get all genres
        :param limit: The limit
        :param offset: The offset
        :param keyword: The keyword
        :return: The genres
        """
        genres = (
            Genre.query.filter_by(is_deleted=False)
            .filter(Genre.name.ilike("%{keyword}%".format(keyword=keyword)))
            .offset(offset=offset)
            .limit(limit=limit)
            .all()
        )

        return [genre.__str__() for genre in genres]

    def get_by_id(self, id: int) -> Genre:
        """
        Get a genre by ID
        :param id: The genre ID
        :return: The genre
        """
        genre = Genre.query.get(id)
        if not genre:
            raise ValueError("Genre not found")
        return genre.__str__()

    def store(self, data: dict) -> Genre:
        """
        Store a new genre
        :param data: The genre data
        :return: The stored genre
        """
        name = data.get("name")
        permalink = data.get("permalink")

        existing_genre = Genre.query.filter_by(
            permalink=permalink, is_deleted=False
        ).first()
        if existing_genre:
            raise ValueError("Permalink already exists")

        genre = Genre(name, permalink)
        return genre.__str__()

    def update(self, id: int, data: dict) -> Genre:
        """
        Update a genre
        :param id: The genre ID
        :param data: The genre data
        :return: The updated genre
        """
        genre = Genre.query.get(id)
        if not genre:
            raise ValueError("Genre not found")

        return genre.update(**data).__str__()

    def destroy(self, id: int) -> None:
        """
        Destroy a genre
        :param id: The genre ID
        :return: The destroyed genre
        """
        genre = Genre.query.get(id)
        if not genre:
            raise ValueError("Genre not found")

        genre.delete()
