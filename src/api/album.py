from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from pydantic import BaseModel

from src.controllers import AlbumController
from src.utils import PaginationParams, response

router = APIRouter(prefix="/album", tags=["album"])


# Định nghĩa Pydantic models thay vì flask-restx models
class AlbumCreate(BaseModel):
    name: str
    image: Optional[str] = None
    permalink: str
    album_type: str
    release_date: str
    artist_ids: Optional[List[int]] = None


class AlbumUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    permalink: Optional[str] = None
    album_type: Optional[str] = None
    release_date: Optional[str] = None
    artist_ids: Optional[List[int]] = None


@router.get("/")
async def get_albums(pagination: PaginationParams = Depends()):
    """
    Lấy danh sách album
    """
    try:
        ctl = AlbumController()
        result = ctl.get_all(pagination.limit, pagination.page, pagination.keyword)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
async def create_album(album: AlbumCreate):
    """
    Tạo album mới
    """
    try:
        ctl = AlbumController()
        result = ctl.store(album.model_dump())
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
async def get_album(id: int = Path(..., description="ID của album")):
    """
    Lấy thông tin album theo ID
    """
    try:
        ctl = AlbumController()
        result = ctl.get_by_id(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}")
async def update_album(
    id: int = Path(..., description="ID của album"), album: AlbumUpdate = Body(...)
):
    """
    Cập nhật thông tin album
    """
    try:
        ctl = AlbumController()
        result = ctl.update(id, album.model_dump(exclude_unset=True))
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
async def delete_album(id: int = Path(..., description="ID của album")):
    """
    Xóa album
    """
    try:
        ctl = AlbumController()
        result = ctl.delete(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
