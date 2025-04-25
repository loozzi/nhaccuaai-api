"""
File này không còn cần thiết vì FastAPI đã có cơ chế xử lý query params riêng.
Tuy nhiên giữ lại hàm pagination_response để sử dụng trong các controllers.
"""


def pagination_response(data, limit, page, total):
    return {
        "items": data,
        "meta": {
            "limit": limit,
            "page": page,
            "total": total,
        },
    }
