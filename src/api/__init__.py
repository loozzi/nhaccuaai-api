from fastapi import APIRouter

router = APIRouter()

# Import các router modules
from .album import router as album_router
from .artist import router as artist_router
from .auth import router as auth_router
from .genre import router as genre_router
from .track import router as track_router

# Đăng ký các router
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(genre_router, prefix="/genre", tags=["genre"])
router.include_router(artist_router, prefix="/artist", tags=["artist"])
router.include_router(album_router, prefix="/album", tags=["album"])
router.include_router(track_router, prefix="/track", tags=["track"])
