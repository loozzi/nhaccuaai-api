from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import time
from typing import Callable
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomMiddleware:
    """
    Custom middleware cho FastAPI
    """
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info(f"Request processed in {process_time:.4f}s: {request.method} {request.url.path}")
            return response
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "status": 500, 
                    "message": "Database error occurred",
                    "data": None
                }
            )
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "status": 500,
                    "message": "An unexpected error occurred",
                    "data": None
                }
            )