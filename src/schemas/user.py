from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# Schema cơ bản cho User
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email của người dùng")
    name: str = Field(..., description="Tên người dùng")
    
    class Config:
        orm_mode = True

# Schema cho việc tạo mới User
class UserCreate(UserBase):
    password: str = Field(..., description="Mật khẩu người dùng")

# Schema cho việc cập nhật User
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email của người dùng")
    name: Optional[str] = Field(None, description="Tên người dùng")
    password: Optional[str] = Field(None, description="Mật khẩu người dùng")
    
    class Config:
        orm_mode = True

# Schema để hiển thị thông tin User
class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True

# Schema cho việc đăng nhập User
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email của người dùng")
    password: str = Field(..., description="Mật khẩu người dùng")

# Schema cho token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schema cho thông tin token
class TokenData(BaseModel):
    email: Optional[str] = None