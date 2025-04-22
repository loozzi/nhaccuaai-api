from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src import get_db
from src.controllers import AuthController
from src.schemas.user import Token, UserLogin
from src.utils.response import response

router = APIRouter()

@router.post("/sign-in", response_model=dict)
async def sign_in(token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Đăng nhập với token
    """
    try:
        controller = AuthController()
        result = controller.sign_in(token, db)
        return response(200, "Success", result)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sign-up", response_model=dict)
async def sign_up(token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Đăng ký với token
    """
    try:
        controller = AuthController()
        result = controller.sign_up(token, db)
        return response(200, "Success", result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh-token", response_model=dict)
async def refresh_token(token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Làm mới token
    """
    try:
        controller = AuthController()
        result = controller.refresh_token(token, db)
        return response(200, "Success", result)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Đăng nhập để lấy access token
    """
    try:
        controller = AuthController()
        user = controller.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = controller.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
