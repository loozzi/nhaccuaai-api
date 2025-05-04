from fastapi import APIRouter, Query, Request

from src.controllers import BrowseController
from src.utils import pagination_response, response

router = APIRouter(prefix="/browse", tags=["browse"])


@router.get("/")
def get(
    request: Request,
    limit: int = Query(10, description="Số lượng kết quả trả về"),
    page: int = Query(1, description="Trang hiện tại"),
    keyword: str = Query("", description="Từ khóa tìm kiếm"),
):
    """
    Lấy danh sách bài hát
    """
    try:
        # Simulate a controller call to get all tracks
        # ctl = TrackController()
        # result = ctl.get_all(limit, page, keyword)
        result = {
            "limit": limit,
            "page": page,
            "keyword": keyword,
            "tracks": [],  # Placeholder for actual track data
        }
        return {"status": 200, "message": "Success", "data": result}
    except Exception as e:
        return {"status": 400, "message": str(e)}


@router.get("/search")
def search(
    request: Request,
    keyword: str = Query(..., description="Từ khóa tìm kiếm"),
    limit: int = Query(10, description="Số lượng kết quả trả về"),
    page: int = Query(1, description="Trang hiện tại"),
):
    """
    Tìm kiếm bài hát theo từ khóa
    """
    try:
        # Simulate a controller call to search tracks
        ctl = BrowseController()
        result = ctl.search(keyword, limit, page)

        return response(
            200,
            "Success",
            pagination_response(
                data=result["data"],
                limit=limit,
                page=page,
                total=result["total"],  # Placeholder for actual total count
            ),
        )
    except Exception as e:
        return {"status": 400, "message": str(e)}
