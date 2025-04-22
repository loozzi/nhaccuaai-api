from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field
from src.utils.enums import TrackType

# Schema cơ bản cho Track
class TrackBase(BaseModel):
    name: str = Field(..., description="Tên bài hát")
    file_url: str = Field(..., description="URL file âm thanh")
    duration: int = Field(..., description="Thời lượng bài hát tính bằng mili giây")
    permalink: str = Field(..., description="Đường dẫn tĩnh")
    type: Optional[str] = Field(None, description="Loại bài hát")
    release_date: Optional[date] = Field(None, description="Ngày phát hành")
    track_number: Optional[int] = Field(None, description="Số thứ tự trong album")
    image: Optional[str] = Field(None, description="URL hình ảnh")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

# Schema cho việc tạo mới Track
class TrackCreate(TrackBase):
    album_id: int = Field(..., description="ID của album")
    artists: List[int] = Field(..., description="Danh sách ID của các nghệ sĩ")

# Schema cho việc cập nhật Track
class TrackUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Tên bài hát")
    file_url: Optional[str] = Field(None, description="URL file âm thanh")
    duration: Optional[int] = Field(None, description="Thời lượng bài hát tính bằng mili giây")
    permalink: Optional[str] = Field(None, description="Đường dẫn tĩnh")
    type: Optional[str] = Field(None, description="Loại bài hát")
    release_date: Optional[date] = Field(None, description="Ngày phát hành")
    track_number: Optional[int] = Field(None, description="Số thứ tự trong album")
    image: Optional[str] = Field(None, description="URL hình ảnh")
    album_id: Optional[int] = Field(None, description="ID của album")
    artists: Optional[List[int]] = Field(None, description="Danh sách ID của các nghệ sĩ")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

# Schema để hiển thị thông tin Track
class TrackResponse(TrackBase):
    id: int
    album_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Schema cho phản hồi API
class ApiResponse(BaseModel):
    status: int
    message: str
    data: Optional[dict] = None