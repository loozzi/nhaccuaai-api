from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path
from pydantic import BaseModel

from src.controllers import ArtistController
from src.utils import PaginationParams, response

router = APIRouter(prefix="/artist", tags=["artist"])


# Định nghĩa Pydantic models thay vì flask-restx models
class GenreList(BaseModel):
    genres: Optional[List[int]] = None


class ArtistCreate(BaseModel):
    name: str
    image: str
    permalink: str
    genres: Optional[List[int]] = None


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    permalink: Optional[str] = None
    genres: Optional[List[int]] = None


@router.get("/")
async def get_artists(pagination: PaginationParams = Depends()):
    """
    Lấy danh sách nghệ sĩ
    """
    try:
        ctl = ArtistController()
        result = ctl.get_all(pagination.limit, pagination.page, pagination.keyword)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.post("/")
async def create_artist(artist: ArtistCreate):
    """
    Tạo nghệ sĩ mới
    """
    try:
        ctl = ArtistController()
        result = ctl.store(artist.model_dump())
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/{id}")
async def get_artist(id: int = Path(..., description="ID của nghệ sĩ")):
    """
    Lấy thông tin nghệ sĩ theo ID
    """
    try:
        ctl = ArtistController()
        result = ctl.get_by_id(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.put("/{id}")
async def update_artist(
    id: int = Path(..., description="ID của nghệ sĩ"), artist: ArtistUpdate = Body(...)
):
    """
    Cập nhật thông tin nghệ sĩ
    """
    try:
        ctl = ArtistController()
        result = ctl.update(id, artist.model_dump(exclude_unset=True))
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.delete("/{id}")
async def delete_artist(id: int = Path(..., description="ID của nghệ sĩ")):
    """
    Xóa nghệ sĩ
    """
    try:
        ctl = ArtistController()
        result = ctl.destroy(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))
