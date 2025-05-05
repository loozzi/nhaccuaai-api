import os
from datetime import date
from typing import Optional

from fastapi import APIRouter, Body, Path, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.controllers import TrackController
from src.utils import response

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
        return response(400, str(e))


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
        return response(400, str(e))


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
        return response(400, str(e))


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
        return response(400, str(e))


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
        return response(400, str(e))


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
        return response(400, str(e))


@router.get("/play/{permalink}")
async def play_track(
    permalink: str = Path(..., description="Permalink của bài hát"),
    request: Request = None,
):
    """
    Phát bài hát theo permalink
    """
    try:
        track = TrackController().get_by_permalink(permalink)
        headers = {
            "Content-Type": "audio/mpeg",
            "Accept-Ranges": "bytes",
            "Content-Disposition": "inline; filename={0}.mp3".format(track["name"]),
        }

        file_path = "songs/{}.mp3".format(permalink)
        file_size = os.path.getsize(file_path)

        status_code = 200
        range_start = 0
        range_end = file_size - 1
        range_header = request.headers.get("Range")
        if range_header:
            try:
                range_str = range_header.replace("bytes=", "").split("-")
                range_start = int(range_str[0]) if range_str[0] else 0
                range_end = int(range_str[1]) if range_str[1] else file_size - 1
            except (ValueError, IndexError):
                raise Exception("Invalid Range header")

            # Đảm bảo range hợp lệ
            if (
                range_start >= file_size
                or range_end >= file_size
                or range_start > range_end
            ):
                raise Exception("Range not satisfiable")

            # Cập nhật headers cho phản hồi Range
            status_code = 206  # Partial Content
            headers.update(
                {
                    "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
                    "Content-Length": str(range_end - range_start + 1),
                }
            )

        def iterfile():
            with open(file_path, mode="rb") as file:
                file.seek(range_start)  # Di chuyển con trỏ file đến vị trí bắt đầu
                remaining_bytes = range_end - range_start + 1
                while remaining_bytes > 0:
                    chunk_size = min(
                        8192, remaining_bytes
                    )  # Đọc tối đa 8KB hoặc phần còn lại
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
                    remaining_bytes -= len(chunk)

        return StreamingResponse(
            iterfile(),
            media_type="audio/mpeg",
            headers=headers,
            status_code=status_code,
        )
    except Exception as e:
        return response(400, str(e))
