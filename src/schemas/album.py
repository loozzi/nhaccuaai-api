from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

# Schema cơ bản cho Album
class AlbumBase(BaseModel):
    name: str = Field(..., description="Tên album")
    permalink: str = Field(..., description="Đường dẫn tĩnh")
    image: Optional[str] = Field(None, description="URL hình ảnh")
    release_date: Optional[date] = Field(None, description="Ngày phát hành")
    
    class Config:
        orm_mode = True

# Schema cho việc tạo mới Album
class AlbumCreate(AlbumBase):
    artists: List[int] = Field(..., description="Danh sách ID của các nghệ sĩ")

# Schema cho việc cập nhật Album
class AlbumUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Tên album")
    permalink: Optional[str] = Field(None, description="Đường dẫn tĩnh")
    image: Optional[str] = Field(None, description="URL hình ảnh")
    release_date: Optional[date] = Field(None, description="Ngày phát hành")
    artists: Optional[List[int]] = Field(None, description="Danh sách ID của các nghệ sĩ")
    
    class Config:
        orm_mode = True

# Schema để hiển thị thông tin Album
class AlbumResponse(AlbumBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True