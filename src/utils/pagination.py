from flask_restx import reqparse

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    "limit", type=int, default=10, help="Number of items per page"
)
pagination_parser.add_argument("page", type=int, default=1, help="Page number")
pagination_parser.add_argument("keyword", type=str, default="", help="Search keyword")


def pagination_response(data, limit, page, total):
    return {
        "data": data,
        "meta": {
            "limit": limit,
            "page": page,
            "total": total,
        },
    }
