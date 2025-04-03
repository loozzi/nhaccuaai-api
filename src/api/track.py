from flask_restx import Namespace, Resource, fields

from src.controllers import AlbumController, ArtistController, TrackController
from src.utils import pagination_parser, response
from src.utils.enums import TrackType

track_ns = Namespace("track", description="Track operations")

track_model = track_ns.model(
    "Track",
    {
        "name": fields.String(required=True, description="The track name"),
        "file_url": fields.String(required=True, description="The track file URL"),
        "duration": fields.Integer(required=True, description="The track duration"),
        "permalink": fields.String(required=True, description="The track permalink"),
        "type": fields.String(
            description="The track type", enum=[e.value for e in TrackType]
        ),
        "release_date": fields.Date(description="The track release date"),
        "track_number": fields.Integer(description="The track number"),
    },
)

track_update_model = track_ns.model(
    "TrackUpdate",
    {
        "name": fields.String(description="The track name"),
        "file_url": fields.String(description="The track file URL"),
        "duration": fields.Integer(description="The track duration"),
        "permalink": fields.String(description="The track permalink"),
        "type": fields.String(
            description="The track type", enum=[e.value for e in TrackType]
        ),
        "release_date": fields.Date(description="The track release date"),
        "track_number": fields.Integer(description="The track number"),
    },
)


@track_ns.route("/")
class TrackApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = TrackController()

    @track_ns.expect(pagination_parser)
    @track_ns.response(200, "Success")
    @track_ns.response(400, "Bad Request")
    def get(self):
        try:
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

    @track_ns.expect(track_model)
    @track_ns.response(200, "Success")
    @track_ns.response(400, "Bad Request")
    def post(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.store(track_ns.payload),
            )
        except Exception as e:
            return response(400, str(e))


@track_ns.route("/<int:id>")
class TrackWithIdApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl: TrackController = TrackController()

    @track_ns.response(200, "Success")
    @track_ns.response(400, "Bad Request")
    def put(self, id: int):
        try:
            return response(
                200,
                "Success",
                self.ctl.update(id, track_ns.payload),
            )
        except Exception as e:
            return response(400, str(e))

    @track_ns.response(200, "Success")
    @track_ns.response(400, "Bad Request")
    def delete(self, id: int):
        try:
            return response(
                200,
                "Success",
                self.ctl.destroy(id),
            )
        except Exception as e:
            return response(400, str(e))


@track_ns.route("/<string:permalink>")
class TrackWithPermalinkApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl: TrackController = TrackController()

    @track_ns.response(200, "Success")
    @track_ns.response(400, "Bad Request")
    def get(self, permalink: str):
        try:
            return response(
                200,
                "Success",
                self.ctl.get_by_permalink(permalink),
            )
        except Exception as e:
            return response(400, str(e))


@track_ns.route("/crawl/<string:link>")
class CrawlerApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl: TrackController = TrackController()
        self.album_ctl: AlbumController = AlbumController()
        self.artist_ctl: ArtistController = ArtistController()

    @track_ns.response(200, "Success")
    @track_ns.response(400, "Bad Request")
    def get(self, link: str):
        try:
            track_data = self.ctl.crawl(link)

            # self.ctl.store(track_data)

            return response(200, "Success", track_data)
        except Exception as e:
            return response(400, str(e))
