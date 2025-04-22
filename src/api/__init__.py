from flask import Blueprint

__api = Blueprint("api", __name__, url_prefix="/api")

# Các router sẽ được import từ main __init__.py
# Không cần thiết phải định nghĩa namespace nữa vì đã chuyển sang FastAPI router
