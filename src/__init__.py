import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import _config

# Khởi tạo Flask app (vẫn cần cho SQLAlchemy và Migrate)
flask_app = Flask(__name__)
bcrypt = Bcrypt(flask_app)

config = _config.getProdConfig()
if len(sys.argv) > 1 and sys.argv[1] == "--dev":
    config = _config.getDevConfig()

env = config.ENV

flask_app.config["SQLALCHEMY_DATABASE_URI"] = env.SQLALCHEMY_DATABASE_URI
flask_app.env = env.ENV_NAME

# Khởi tạo database với Flask
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

# Khởi tạo FastAPI app
app = FastAPI(
    title="NhacCuaAi API",
    description="NhacCuaAi API Documentation",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


# Tạo middleware để đảm bảo mỗi request đều có Flask app context
@app.middleware("http")
async def flask_app_context(request: Request, call_next):
    # Sử dụng app_context để đảm bảo mỗi request đều có context
    with flask_app.app_context():
        # Thực hiện request trong context của Flask
        response = await call_next(request)
        return response


# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from .api.album import router as album_router
from .api.artist import router as artist_router
from .api.auth import router as auth_router
from .api.genre import router as genre_router
from .api.track import router as track_router

# Import models
from .models import *

# Thêm routers vào app
prefix = _config.PREFIX_URL
app.include_router(auth_router, prefix=prefix)
app.include_router(genre_router, prefix=prefix)
app.include_router(artist_router, prefix=prefix)
app.include_router(album_router, prefix=prefix)
app.include_router(track_router, prefix=prefix)


# Sử dụng on_event để thiết lập và giải phóng tài nguyên
@app.on_event("startup")
async def startup_event():
    # Push application context khi ứng dụng bắt đầu
    flask_app.app_context().push()


@app.on_event("shutdown")
async def shutdown_event():
    # Không cần pop context vì nó sẽ tự động được dọn dẹp khi ứng dụng kết thúc
    pass
