from flask_restx import Namespace, Resource, fields

from src.controllers import GenreController
from src.utils import pagination_parser, response

genre_ns = Namespace("genre", description="Genre operations")

genre_model = genre_ns.model(
    "Genre",
    {
        "name": fields.String(required=True, description="The genre name"),
        "permalink": fields.String(required=True, description="The genre permalink"),
    },
)

genre_update_model = genre_ns.model(
    "GenreUpdate",
    {
        "name": fields.String(description="The genre name"),
        "permalink": fields.String(description="The genre permalink"),
    },
)


@genre_ns.route("/")
class GenreApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = GenreController()

    @genre_ns.expect(pagination_parser)
    @genre_ns.response(200, "Success")
    @genre_ns.response(400, "Bad Request")
    @genre_ns.response(401, "Unauthorized")
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

    @genre_ns.expect(genre_model)
    @genre_ns.response(200, "Success")
    @genre_ns.response(400, "Bad Request")
    @genre_ns.response(401, "Unauthorized")
    def post(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.store(genre_ns.payload),
            )
        except Exception as e:
            return response(400, str(e))


@genre_ns.route("/<int:id>")
class GenreWithIdApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = GenreController()

    @genre_ns.response(200, "Success")
    @genre_ns.response(400, "Bad Request")
    @genre_ns.response(401, "Unauthorized")
    @genre_ns.response(404, "Not Found")
    def get(self, id):
        try:
            return response(
                200,
                "Success",
                self.ctl.get_by_id(id),
            )
        except Exception as e:
            return response(400, str(e))

    @genre_ns.expect(genre_update_model)
    @genre_ns.response(200, "Success")
    @genre_ns.response(400, "Bad Request")
    @genre_ns.response(401, "Unauthorized")
    @genre_ns.response(404, "Not Found")
    def put(self, id):
        try:
            return response(
                200,
                "Success",
                self.ctl.update(id, genre_ns.payload),
            )
        except Exception as e:
            return response(400, str(e))

    @genre_ns.response(200, "Success")
    @genre_ns.response(400, "Bad Request")
    @genre_ns.response(401, "Unauthorized")
    @genre_ns.response(404, "Not Found")
    def delete(self, id):
        try:
            return response(
                200,
                "Success",
                self.ctl.destroy(id),
            )
        except Exception as e:
            return response(400, str(e))
