from typing import Optional, List
from pydantic import BaseModel, Field

# Schema cơ bản cho Artist
class ArtistBase(BaseModel):
    name: str = Field(..., description="Tên nghệ sĩ")
    permalink: str = Field(..., description="Đường dẫn tĩnh")
    image: Optional[str] = Field(None, description="URL hình ảnh")
    
    class Config:
        orm_mode = True

# Schema cho việc tạo mới Artist
class ArtistCreate(ArtistBase):
    genres: Optional[List[int]] = Field(None, description="Danh sách ID thể loại")

# Schema cho việc cập nhật Artist
class ArtistUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Tên nghệ sĩ")
    permalink: Optional[str] = Field(None, description="Đường dẫn tĩnh")
    image: Optional[str] = Field(None, description="URL hình ảnh")
    genres: Optional[List[int]] = Field(None, description="Danh sách ID thể loại")
    
    class Config:
        orm_mode = True

# Schema để hiển thị thông tin Artist
class ArtistResponse(ArtistBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True