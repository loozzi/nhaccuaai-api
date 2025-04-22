from typing import Optional, List
from pydantic import BaseModel, Field

# Schema cơ bản cho Genre
class GenreBase(BaseModel):
    name: str = Field(..., description="Tên thể loại")
    
    class Config:
        orm_mode = True

# Schema cho việc tạo mới Genre
class GenreCreate(GenreBase):
    pass

# Schema cho việc cập nhật Genre
class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Tên thể loại")
    
    class Config:
        orm_mode = True

# Schema để hiển thị thông tin Genre
class GenreResponse(GenreBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True