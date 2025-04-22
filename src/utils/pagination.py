from typing import List, Dict, Any
from fastapi import Query

# Không cần pagination parser trong FastAPI vì chúng ta có thể dùng Query parameters trực tiếp trong các endpoint

def pagination_response(data: List[Any], limit: int, page: int, total: int) -> Dict:
    """
    Create a pagination response
    :param data: The data
    :param limit: The limit per page
    :param page: The current page
    :param total: The total number of items
    :return: The pagination response
    """
    return {
        "data": data,
        "meta": {
            "limit": limit,
            "page": page,
            "total": total,
        },
    }
