import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

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

# Đảm bảo ứng dụng Flask luôn có context khi chạy FastAPI
@flask_app.before_request
def create_context():
    flask_app.app_context().push()

# Đảm bảo context Flask luôn tồn tại cho FastAPI
ctx = flask_app.app_context()
ctx.push()

# Khởi tạo FastAPI app
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

# Import models
from .models import *

# Import routers
from .api.album import router as album_router
from .api.artist import router as artist_router
from .api.auth import router as auth_router
from .api.genre import router as genre_router
from .api.track import router as track_router

# Thêm routers vào app
prefix = _config.PREFIX_URL
app.include_router(auth_router, prefix=prefix)
app.include_router(genre_router, prefix=prefix)
app.include_router(artist_router, prefix=prefix)
app.include_router(album_router, prefix=prefix)
app.include_router(track_router, prefix=prefix)

# Event khi ứng dụng shutdown để đóng context Flask
@app.on_event("shutdown")
def shutdown_event():
    if ctx:
        ctx.pop()
