import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .config import _config
from .utils.middleware import CustomMiddleware

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="NhacCuaAi API",
    description="NhacCuaAi API Documentation",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thêm custom middleware
app.add_middleware(CustomMiddleware)

# Lấy cấu hình
config = _config.getProdConfig()
if len(sys.argv) > 1 and sys.argv[1] == "--dev":
    config = _config.getDevConfig()

env = config.ENV

# Thiết lập SQLAlchemy
SQLALCHEMY_DATABASE_URI = env.SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Hàm dependency để tạo DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import các API routes
from .api import router as api_router

# Đăng ký router
app.include_router(api_router, prefix=_config.PREFIX_URL)

# Import models
from .models import *
