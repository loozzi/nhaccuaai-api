from typing import Optional

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

from src.controllers import GenreController
from src.utils import response

router = APIRouter(prefix="/genre", tags=["genre"])


# Định nghĩa Pydantic models
class GenreCreate(BaseModel):
    name: str
    permalink: str


class GenreUpdate(BaseModel):
    name: Optional[str] = None
    permalink: Optional[str] = None


@router.get("/")
async def get_genres(
    limit: int = Query(10, description="Số lượng kết quả trả về"),
    page: int = Query(1, description="Trang hiện tại"),
    keyword: str = Query("", description="Từ khóa tìm kiếm"),
):
    """
    Lấy danh sách thể loại
    """
    try:
        ctl = GenreController()
        result = ctl.get_all(limit, page, keyword)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.post("/")
async def create_genre(genre: GenreCreate):
    """
    Tạo thể loại mới
    """
    try:
        ctl = GenreController()
        result = ctl.store(genre.model_dump())
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/{id}")
async def get_genre(id: int = Path(..., description="ID của thể loại")):
    """
    Lấy thông tin thể loại theo ID
    """
    try:
        ctl = GenreController()
        result = ctl.get_by_id(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.put("/{id}")
async def update_genre(
    id: int = Path(..., description="ID của thể loại"), genre: GenreUpdate = Body(...)
):
    """
    Cập nhật thông tin thể loại
    """
    try:
        ctl = GenreController()
        result = ctl.update(id, genre.model_dump(exclude_unset=True))
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.delete("/{id}")
async def delete_genre(id: int = Path(..., description="ID của thể loại")):
    """
    Xóa thể loại
    """
    try:
        ctl = GenreController()
        result = ctl.destroy(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))
