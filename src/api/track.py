from datetime import date
from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query
from pydantic import BaseModel

from src.controllers import TrackController
from src.utils import response
from src.utils.enums import TrackType

router = APIRouter(prefix="/track", tags=["track"])


# Định nghĩa Pydantic models
class TrackCreate(BaseModel):
    name: str
    file_url: str
    duration: int
    permalink: str
    type: Optional[str] = None  # Enum values from TrackType
    release_date: Optional[date] = None
    track_number: Optional[int] = None


class TrackUpdate(BaseModel):
    name: Optional[str] = None
    file_url: Optional[str] = None
    duration: Optional[int] = None
    permalink: Optional[str] = None
    type: Optional[str] = None  # Enum values from TrackType
    release_date: Optional[date] = None
    track_number: Optional[int] = None


@router.get("/")
async def get_tracks(
    limit: int = Query(10, description="Số lượng kết quả trả về"),
    page: int = Query(1, description="Trang hiện tại"),
    keyword: str = Query("", description="Từ khóa tìm kiếm"),
):
    """
    Lấy danh sách bài hát
    """
    try:
        ctl = TrackController()
        result = ctl.get_all(limit, page, keyword)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
async def create_track(track: TrackCreate):
    """
    Tạo bài hát mới
    """
    try:
        ctl = TrackController()
        result = ctl.store(track.model_dump())
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}")
async def update_track(
    id: int = Path(..., description="ID của bài hát"), track: TrackUpdate = Body(...)
):
    """
    Cập nhật thông tin bài hát
    """
    try:
        ctl = TrackController()
        result = ctl.update(id, track.model_dump(exclude_unset=True))
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
async def delete_track(id: int = Path(..., description="ID của bài hát")):
    """
    Xóa bài hát
    """
    try:
        ctl = TrackController()
        result = ctl.destroy(id)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/crawl/{link}")
async def crawl_track(link: str = Path(..., description="Link bài hát cần crawl")):
    """
    Crawl thông tin bài hát từ link
    """
    try:
        ctl = TrackController()
        result = ctl.crawl(link)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/by-permalink/{permalink}")
async def get_track_by_permalink(
    permalink: str = Path(..., description="Permalink của bài hát")
):
    """
    Lấy thông tin bài hát theo permalink
    """
    try:
        ctl = TrackController()
        result = ctl.get_by_permalink(permalink)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
