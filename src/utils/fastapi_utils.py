"""
File này cung cấp các hàm và lớp tiện ích cho việc chuyển đổi từ Flask-RestX sang FastAPI
"""

from typing import Any, Dict, List, Optional, Union

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel


class PaginationParams:
    """
    Lớp xử lý tham số phân trang, sử dụng cho dependency injection trong FastAPI
    """

    def __init__(self, limit: int = 10, page: int = 1, keyword: str = ""):
        self.limit = limit
        self.page = page
        self.keyword = keyword
