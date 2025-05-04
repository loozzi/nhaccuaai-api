import datetime
import os

import eyed3
import requests
import requests as req
import spotipy
import yt_dlp
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

from src import env
from src.models import (
    Album,
    AlbumArtist,
    Artist,
    ArtistGenre,
    Genre,
    Track,
    TrackArtist,
)
from src.utils import gen_permalink


class Song:
    def __init__(self, sp: spotipy.Spotify, link: str):
        self.sp = sp
        self.spotify = self.sp.track(link)
        self.id = self.spotify["id"]
        self.spotify_link = self.spotify["external_urls"]["spotify"]
        self.track_name = self.spotify["name"]
        self.artists_list = self.spotify["artists"]
        self.artist_name = self.artists_list[0]["name"]
        self.artists = self.spotify["artists"]
        self.track_number = self.spotify["track_number"]
        self.album = self.spotify["album"]
        self.album_id = self.album["id"]
        self.album_name = self.album["name"]
        self.release_date = self.spotify["album"]["release_date"]
        self.duration = int(self.spotify["duration_ms"])
        self.duration_to_seconds = int(self.duration / 1000)
        self.album_cover = self.spotify["album"]["images"][0]["url"]
        self.path = "./songs"
        self.file = f"{self.path}/{self.id}.mp3"
        self.uri = self.spotify["uri"]

    def features(self):
        if len(self.artists) > 1:
            features = "(Ft."
            for artistPlace in range(0, len(self.artists)):
                try:
                    if artistPlace < len(self.artists) - 2:
                        artistft = self.artists[artistPlace + 1]["name"] + ", "
                    else:
                        artistft = self.artists[artistPlace + 1]["name"] + ")"
                    features += artistft
                except IndexError:
                    features += ""
                    pass
        else:
            features = ""
        return features

    def convert_time_duration(self):
        target_datetime_ms = self.duration
        base_datetime = datetime.datetime(1900, 1, 1)
        delta = datetime.timedelta(0, 0, 0, target_datetime_ms)

        return base_datetime + delta

    def download_song_cover(self):
        response = requests.get(self.album_cover)
        image_file_name = f"./covers/{self.id}.png"
        image = open(image_file_name, "wb")
        image.write(response.content)
        image.close()
        return image_file_name

    def yt_link(self):
        results = list(
            YoutubeSearch(str(self.track_name + " " + self.artist_name)).to_dict()
        )
        time_duration = self.convert_time_duration()
        yt_url = None

        for yt in results:
            yt_time = yt["duration"]
            yt_time = datetime.datetime.strptime(yt_time, "%M:%S")
            difference = abs((yt_time - time_duration).total_seconds())

            if difference <= 3:
                yt_url = yt["url_suffix"]
                break
        if yt_url is None:
            return None

        yt_link = str("https://www.youtube.com/" + yt_url)
        return yt_link

    def yt_download(self, yt_link=None):
        options = {
            # PERMANENT options
            "format": "bestaudio/best",
            "keepvideo": False,
            "outtmpl": self.file.replace(".mp3", ""),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
        }
        if yt_link is None:
            yt_link = self.yt_link()
        with yt_dlp.YoutubeDL(options) as mp3:
            mp3.download([yt_link])

    def lyrics(self):
        return ""

    def song_meta_data(self):
        mp3 = eyed3.load(self.file)
        if mp3.tag is None:
            mp3.initTag()
        mp3.tag.artist_name = self.artist_name
        mp3.tag.contributing_artists = self.features()
        mp3.tag.album_name = self.album_name or self.track_name
        mp3.tag.album_artist = self.artist_name
        mp3.tag.title = self.track_name + self.features()
        mp3.tag.track_num = self.track_number

        def get_date_release():
            s = self.release_date.split("-")
            return int(s[0]), int(s[1]), int(s[2])

        mp3.tag.recording_date = eyed3.core.Date(*get_date_release())

        mp3.tag.images.set(
            3, open(self.download_song_cover(), "rb").read(), "image/png"
        )
        mp3.tag.save()

    def download(self, yt_link=None):
        if os.path.exists(self.file):
            print(
                f"[SPOTIFY] Song Already Downloaded: {self.track_name} by {self.artist_name}"
            )
            return self.file
        try:
            # print(f'[YOUTUBE] Downloading {self.track_name} by {self.artist_name}...')
            self.yt_download(yt_link=yt_link)
            # print(f'[SPOTIFY] Song Metadata: {self.track_name} by {self.artist_name}')
            self.song_meta_data()
            # print(f'[SPOTIFY] Song Downloaded: {self.track_name} by {self.artist_name}')
            return self.file
        except Exception as e:
            print(
                f"[SPOTIFY] Error Downloading {self.track_name} by {self.artist_name}"
            )
            print(e)
            return None


class Crawler:
    def __init__(self):
        self.sp = self.__get_sp()

    def features(self):
        """
        Get the features
        :return: The features
        """
        response = req.get("https://api.spotify.com/v1/audio-features")
        return response.json()

    def song_info(self, id: str) -> dict:
        """
        Get the song info
        :param id: The song ID
        :return: The song info
        """
        song = self.sp.track(id)
        if not song:
            raise ValueError("Song not found")

        # Download the song and generate file link
        song_obj = Song(self.sp, id)
        file_name = song_obj.download()
        if file_name is None:
            raise ValueError("Song not found")
        file_url = os.path.abspath(file_name)

        return {
            "id": song["id"],
            "name": song["name"],
            "artists": [self.artist_info(artist["id"]) for artist in song["artists"]],
            "album": self.album_info(song["album"]["id"]),
            "duration": song["duration_ms"],
            "type": song["type"],
            "release_date": song["album"]["release_date"],
            "track_number": song["track_number"],
            "file_url": file_url.split("\\")[-1],
            "image": song["album"]["images"][0]["url"],
        }

    def artist_info(self, id: str) -> dict:
        """
        Get the artist info
        :param id: The artist ID
        :return: The artist info
        """
        artist = self.sp.artist(id)
        if not artist:
            raise ValueError("Artist not found")

        return {
            "id": artist["id"],
            "name": artist["name"],
            "image": artist["images"][0]["url"],
            "genres": artist["genres"],
        }

    def album_info(self, id: str) -> dict:
        """
        Get the album info
        :param id: The album ID
        :return: The album info
        """
        album = self.sp.album(id)
        if not album:
            raise ValueError("Album not found")

        return {
            "id": album["id"],
            "name": album["name"],
            "release_date": album["release_date"],
            "image": album["images"][0]["url"],
            "album_type": album["album_type"],
            "artists": [self.artist_info(artist["id"]) for artist in album["artists"]],
        }

    def __get_sp(self) -> spotipy.Spotify:
        client_id = env.SPOTIFY_CLIENT_ID
        client_secret = env.SPOTIFY_CLIENT_SECRET
        if not client_id or not client_secret:
            raise ValueError("Spotify client ID and secret are required.")

        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp


class CrawlerService:
    def __init__(self):
        pass

    def store_track(self, data: dict):
        """
        Store the track
        :param data: The track data
        :return: The track
        """
        track = Track.query.filter_by(permalink=data["permalink"]).first()
        if not track:
            data["release_date"] = datetime.datetime.strptime(
                data["release_date"], "%Y-%m-%d"
            ).date()
            track = Track(
                data["album_id"],
                data["name"],
                data["file_url"],
                data["duration"],
                data["permalink"],
                data["type"],
                data["release_date"],
                data["track_number"],
                data["image"],
            )

        for artist in data["artists"]:
            artist_obj = Artist.query.filter_by(permalink=artist["permalink"]).first()
            if artist_obj:
                TrackArtist(track.id, artist_obj.id)

        return track.__str__()

    def store_album(self, data: dict):
        """
        Store the album
        :param data: The album data
        :return: The album
        """
        album = Album.query.filter_by(permalink=data["permalink"]).first()
        if not album:
            album = Album(
                data["name"],
                data["image"],
                data["permalink"],
                data["album_type"],
                data["release_date"],
            )

        for artist in data["artists"]:
            artist_id = Artist.query.filter_by(permalink=artist["permalink"]).first().id
            AlbumArtist(album.id, artist_id)
        return album.__str__()

    def store_artist(self, data: dict):
        """
        Store the artist
        :param data: The artist data
        :return: The artist
        """
        artist = Artist.query.filter_by(permalink=data["permalink"]).first()
        if not artist:
            artist = Artist(data["name"], data["image"], data["permalink"])

        for genre_id in data["genres"]:
            ArtistGenre(artist.id, genre_id)

        return artist.__str__()

    def store_genres(self, genres: list) -> list:
        """
        Store the genres
        :param genres: The genres
        :return: The genres
        """
        list_genre_ids = []
        for genre_name in genres:
            genre = Genre.query.filter_by(name=genre_name).first()
            if not genre:
                genre = Genre(genre_name, gen_permalink())

            list_genre_ids.append(genre.id)

        return list_genre_ids
