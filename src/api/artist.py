from flask_restx import Namespace, Resource, fields

from src.controllers import ArtistController
from src.utils import pagination_parser, response

artist_ns = Namespace("artist", description="Artist operations")

artist_model = artist_ns.model(
    "Artist",
    {
        "name": fields.String(required=True, description="The artist name"),
        "image": fields.String(required=True, description="The artist image"),
        "permalink": fields.String(required=True, description="The artist permalink"),
        "genres": fields.List(fields.Integer, description="The artist genres id"),
    },
)

artist_update_model = artist_ns.model(
    "ArtistUpdate",
    {
        "name": fields.String(description="The artist name"),
        "image": fields.String(description="The artist image"),
        "permalink": fields.String(description="The artist permalink"),
        "genres": fields.List(fields.Integer, description="The artist genres id"),
    },
)


@artist_ns.route("/")
class ArtistApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = ArtistController()

    @artist_ns.expect(pagination_parser)
    @artist_ns.response(200, "Success")
    @artist_ns.response(400, "Bad Request")
    @artist_ns.response(401, "Unauthorized")
    def get(self):
        try:
            # Get parameters from request.args with default values
            args = pagination_parser.parse_args()
            limit = args.get("limit", 10)
            page = args.get("page", 1)
            keyword = args.get("keyword", "")
            return response(
                200,
                "Success",
                self.ctl.get_all(limit, page, keyword),
            )
        except Exception as e:
            return response(400, str(e))

    @artist_ns.expect(artist_model)
    @artist_ns.response(200, "Success")
    @artist_ns.response(400, "Bad Request")
    @artist_ns.response(401, "Unauthorized")
    def post(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.store(artist_ns.payload),
            )
        except Exception as e:
            return response(400, str(e))


@artist_ns.route("/<int:id>")
class ArtistWithIdApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = ArtistController()

    @artist_ns.response(200, "Success")
    @artist_ns.response(400, "Bad Request")
    @artist_ns.response(401, "Unauthorized")
    @artist_ns.response(404, "Not Found")
    def get(self, id):
        try:
            return response(
                200,
                "Success",
                self.ctl.get_by_id(id),
            )
        except Exception as e:
            return response(400, str(e))

    @artist_ns.expect(artist_update_model)
    @artist_ns.response(200, "Success")
    @artist_ns.response(400, "Bad Request")
    @artist_ns.response(401, "Unauthorized")
    def put(self, id: int):
        # try:
        return response(
            200,
            "Success",
            self.ctl.update(id, artist_ns.payload),
        )

    # except Exception as e:
    #     return response(400, str(e))

    @artist_ns.response(200, "Success")
    @artist_ns.response(400, "Bad Request")
    @artist_ns.response(401, "Unauthorized")
    @artist_ns.response(404, "Not Found")
    def delete(self, id: int):
        try:
            return response(
                200,
                "Success",
                self.ctl.destroy(id),
            )
        except Exception as e:
            return response(400, str(e))
