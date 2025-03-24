from src.models import Artist, ArtistGenre, FavouriteArtist, Genre


class ArtistService:
    def __init__(self):
        pass

    def get_all(self, limit: int, offset: int, keyword: str) -> list:
        """
        Get all artists
        :param limit: The limit
        :param offset: The offset
        :param keyword: The keyword
        :return: The artists
        """
        artists = (
            Artist.query.filter(Artist.name.ilike("%{keyword}".format(keyword=keyword)))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [artist.__str__() for artist in artists]

    def get_by_id(self, id: int) -> Artist:
        """
        Get an artist by ID
        :param id: The artist ID
        :return: The artist
        """
        artist = Artist.query.get(id)
        return artist.__str__()

    def store(self, data: dict) -> Artist:
        """
        Store a new artist
        :param data: The artist data
        :return: The stored artist
        """
        artist_is_exist = Artist.query.filter(
            Artist.permalink == data["permalink"]
        ).first()
        if artist_is_exist:
            raise ValueError("Artist permalink already exists")

        name = data.get("name")
        image = data.get("image")
        permalink = data.get("permalink")
        if not name or not permalink:
            raise ValueError("Missing required fields")

        genres = data.get("genres")
        if genres:
            for genre_id in genres:
                genre_is_exist = Genre.query.get(genre_id)
                if not genre_is_exist:
                    raise ValueError("Genre not found")

        artist = Artist(name=name, image=image, permalink=permalink)
        artist.save()
        if genres:
            for genre_id in genres:
                artist_genre = ArtistGenre(artist_id=artist.id, genre_id=genre_id)
                artist_genre.save()

        artist = artist.__str__()
        artist["genres"] = ArtistGenre.get_genre_artists(artist["id"])

        return artist

    def update(self, id: int, data: dict) -> Artist:
        """
        Update an artist
        :param id: The artist ID
        :param data: The artist data
        :return: The updated artist
        """
        artist = Artist.query.get(id)
        if not artist:
            raise ValueError("Artist not found")

        name = data.get("name")
        image = data.get("image")
        permalink = data.get("permalink")

        if permalink:
            artist_is_exist = Artist.query.filter(
                Artist.permalink == permalink, Artist.id != id
            ).first()
            if artist_is_exist:
                raise ValueError("Artist permalink already exists")

        genres = data.get("genres")
        if genres:
            for genre_id in genres:
                genre_is_exist = Genre.get(genre_id)
                if not genre_is_exist:
                    raise ValueError("Genre not found")

        if name:
            artist.name = name
        if image:
            artist.image = image
        if permalink:
            artist.permalink = permalink
        artist.save()

        if genres:
            ArtistGenre.query.filter(ArtistGenre.artist_id == artist.id).delete()
            for genre_id in genres:
                artist_genre = ArtistGenre(artist_id=artist.id, genre_id=genre_id)
                artist_genre.save()

        artist = artist.__str__()
        artist["genres"] = ArtistGenre.get_artist_genres(artist["id"])

        return artist

    def destroy(self, id: int) -> Artist:
        """
        Destroy an artist
        :param id: The artist ID
        :return: The destroyed artist
        """
        artist = Artist.query.get(id)
        if not artist:
            raise ValueError("Artist not found")

        ArtistGenre.delete_all(artist.id)
        FavouriteArtist.delete_all(artist.id)

        artist.delete()
        return artist.__str__()

    def get_genres(self, artist_id: int) -> list:
        """
        Get all genres of an artist
        :param artist_id: The artist ID
        :return: The genres
        """
        return ArtistGenre.get_artist_genres(artist_id)
