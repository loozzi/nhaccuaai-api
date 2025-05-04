from typing import List

from src.services import AlbumService, ArtistService, BrowseService, TrackService


class BrowseController:
    def __init__(self):
        self.browse_service = BrowseService()
        self.track_service = TrackService()
        self.album_service = AlbumService()
        self.artist_service = ArtistService()

    def get_browse_data(self, user_id):
        return self.browse_service.get_browse_data(user_id)

    def search(self, keyword: str, limit: int, page: int) -> List[object]:
        result = self.browse_service.search(keyword, limit, page)
        response = []
        for row in result["data"]:
            if row["source"] == "track":
                track = self.track_service.get_by_id(row["id"])
                track["artists"] = self.track_service.get_artists(row["id"])
                response.append(
                    {
                        "id": track["id"],
                        "name": track["name"],
                        "image": track["image"],
                        "artists": track["artists"],
                        "permalink": track["permalink"],
                        "type": track["type"],
                        "duration": track["duration"],
                    }
                )
            elif row["source"] == "album":
                album = self.album_service.get_by_id(row["id"])
                response.append(
                    {
                        "id": album["id"],
                        "name": album["name"],
                        "image": album["image"],
                        "artists": self.album_service.get_artists(album["id"]),
                        "permalink": album["permalink"],
                        "type": album["album_type"],
                        "duration": 0,
                    }
                )
            else:
                artist = self.artist_service.get_by_id(row["id"])
                artist["type"] = "artist"
                response.append(artist)

        result["data"] = response
        return result
