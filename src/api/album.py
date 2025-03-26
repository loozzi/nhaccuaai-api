from flask import request
from flask_restx import Namespace, Resource, fields

from src.controllers import AlbumController
from src.utils import pagination_parser, response

album_ns = Namespace("album", description="Albums")

album_model = album_ns.model(
    "Album",
    {
        "name": fields.String(required=True, description="The album name"),
        "image": fields.String(description="The album image"),
        "permalink": fields.String(required=True, description="The album permalink"),
        "album_type": fields.String(required=True, description="The album type"),
        "release_date": fields.String(required=True, description="The release date"),
        "artist_ids": fields.List(fields.Integer, description="The artist IDs"),
    },
)

album_update_model = album_ns.model(
    "AlbumUpdate",
    {
        "name": fields.String(description="The album name"),
        "image": fields.String(description="The album image"),
        "permalink": fields.String(description="The album permalink"),
        "album_type": fields.String(description="The album type"),
        "release_date": fields.String(description="The release date"),
        "artist_ids": fields.List(fields.Integer, description="The artist IDs"),
    },
)


@album_ns.route("/")
class AlbumApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = AlbumController()

    @album_ns.expect(pagination_parser)
    @album_ns.response(200, "Success")
    @album_ns.response(400, "Bad Request")
    @album_ns.response(401, "Unauthorized")
    def get(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.get_all(
                    limit=10,
                    offset=1,
                    keyword="",
                ),
            )

        except Exception as e:
            return response(400, str(e))

    @album_ns.expect(album_model)
    @album_ns.response(200, "Success")
    @album_ns.response(400, "Bad Request")
    @album_ns.response(401, "Unauthorized")
    def post(self):
        try:
            data = request.json
            return response(200, "Success", self.ctl.store(data))
        except Exception as e:
            return response(400, str(e))


@album_ns.route("/<int:id>")
class AlbumWithIdApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = AlbumController()

    @album_ns.response(200, "Success")
    @album_ns.response(400, "Bad Request")
    @album_ns.response(401, "Unauthorized")
    def get(self, id: int):
        try:
            return response(200, "Success", self.ctl.get_by_id(id))
        except Exception as e:
            return response(400, str(e))

    @album_ns.expect(album_update_model)
    @album_ns.response(200, "Success")
    @album_ns.response(400, "Bad Request")
    @album_ns.response(401, "Unauthorized")
    def put(self, id: int):
        try:
            data = request.json
            return response(200, "Success", self.ctl.update(id, data))
        except Exception as e:
            return response(400, str(e))

    @album_ns.response(200, "Success")
    @album_ns.response(400, "Bad Request")
    @album_ns.response(401, "Unauthorized")
    def delete(self, id: int):
        try:
            return response(200, "Success", self.ctl.delete(id))
        except Exception as e:
            return response(400, str(e))
