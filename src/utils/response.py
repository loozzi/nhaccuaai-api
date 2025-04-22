from fastapi.responses import JSONResponse
from typing import Any, Optional

def response(status: int, message: str, data: Any = None) -> dict:
    """
    Create a response
    :param status: The status code
    :param data: The data
    :param message: The message
    :return: The response dictionary
    """
    return {
        "status": status,
        "data": data,
        "message": message,
    }

def json_response(status: int, message: str, data: Any = None) -> JSONResponse:
    """
    Create a JSONResponse with consistent format
    :param status: The status code
    :param data: The data
    :param message: The message
    :return: The JSONResponse
    """
    return JSONResponse(
        status_code=status,
        content={
            "status": status,
            "data": data,
            "message": message,
        }
    )
