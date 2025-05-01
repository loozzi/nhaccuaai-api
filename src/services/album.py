from src.models import Album, AlbumArtist, Artist


class AlbumService:
    def __init__(self):
        pass

    def get_all(self, limit: int, offset: int, keyword: str) -> list:
        """
        Get all albums
        :param limit: The limit
        :param offset: The offset
        :param keyword: The keyword
        :return: The albums
        """
        albums = (
            Album.query.filter(Album.name.ilike("%{keyword}".format(keyword=keyword)))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [album.__str__() for album in albums]

    def get_by_id(self, id: int) -> Album:
        """
        Get an album by ID
        :param id: The album ID
        :return: The album
        """
        album = Album.query.get(id)
        if not album:
            raise ValueError("Album not found")
        return album.__str__()

    def store(self, data: dict) -> Album:
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

        if Album.query.filter(Album.permalink == permalink).first():
            raise ValueError("Album permalink already exists")

        for artist_id in artist_ids:
            artist = Artist.query.get(artist_id)
            if not artist:
                raise ValueError("Artist not found")

        album = Album(
            name=name,
            image=image,
            permalink=permalink,
            album_type=album_type,
            release_date=release_date,
        )
        album.save()

        for artist_id in artist_ids:
            album_artist = AlbumArtist(album_id=album.id, artist_id=artist_id)
            album_artist.save()

        artists = Artist.query.filter(Artist.id.in_(artist_ids)).all()
        artists = [artist.__str__() for artist in artists]

        album = album.__str__()
        album["artists"] = artists

        return album.__str__()

    def update(self, id: int, data: dict) -> Album:
        """
        Update an album
        :param id: The album ID
        :param data: The album data
        :return: The updated album
        """
        album = Album.query.get(id)
        if not album:
            raise ValueError("Album not found")

        permalink = data.get("permalink")
        # TODO: HANDLE UPDATE ARTISTS

        if permalink:
            if Album.query.filter(Album.permalink == permalink, Album.id != id).first():
                raise ValueError("Album permalink already exists")

        album.update(data)
        album.save()
        return album.__str__()

    def destroy(self, id: int) -> None:
        """
        Delete an album
        :param id: The album ID
        """
        album = Album.query.get(id)
        if not album:
            raise ValueError("Album not found")
        album.delete()
        return None

    def get_albums_by_artist_id(self, artist_id: int) -> list:
        """
        Get all albums by artist ID
        :param artist_id: The artist ID
        :return: The albums
        """
        albums = (
            Album.query.join(AlbumArtist)
            .filter(AlbumArtist.artist_id == artist_id)
            .all()
        )
        return [album.__str__() for album in albums]

    def count(self, keyword: str) -> int:
        """
        Count all albums
        :param keyword: The keyword
        :return: The count of albums
        """
        return Album.query.filter(
            Album.name.ilike("%{keyword}".format(keyword=keyword))
        ).count()

    def get_artists(self, album_id: int) -> list:
        """
        Get all artists of a album
        :param album_id: The album ID
        :return: The artists
        """
        artists = AlbumArtist.query.filter_by(album_id=album_id).all()
        if not artists:
            return None
        return list(set([Artist.query.get(artist.artist_id) for artist in artists]))
