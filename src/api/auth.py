from fastapi import APIRouter
from pydantic import BaseModel

from src.controllers import AuthController
from src.utils import response

router = APIRouter(prefix="/auth", tags=["auth"])


# Định nghĩa Pydantic models
class TokenModel(BaseModel):
    token: str


@router.post("/sign-in")
async def sign_in(token_data: TokenModel):
    """
    Đăng nhập với token
    """
    try:
        ctl = AuthController()
        result = ctl.sign_in(token_data.token)
        return response(
            200,
            "Success",
            result,
        )
    except ValueError as e:
        return response(401, str(e))
    except Exception as e:
        return response(400, str(e))


@router.post("/sign-up")
async def sign_up(token_data: TokenModel):
    """
    Đăng ký với token
    """
    try:
        ctl = AuthController()
        result = ctl.sign_up(token_data.token)
        return response(
            200,
            "Success",
            result,
        )
    except Exception as e:
        return response(400, str(e))


@router.post("/refresh-token")
async def refresh_token(token_data: TokenModel):
    """
    Làm mới token
    """
    try:
        ctl = AuthController()
        result = ctl.refresh_token(token_data.token)
        return response(
            200,
            "Success",
            result,
        )
    except ValueError as e:
        return response(401, str(e))
    except Exception as e:
        return response(400, str(e))
