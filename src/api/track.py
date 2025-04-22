from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src import get_db
from src.controllers import TrackController
from src.utils.enums import TrackType

router = APIRouter()

# Định nghĩa các Pydantic models 
class TrackBase(BaseModel):
    name: str = Field(..., description="The track name")
    file_url: str = Field(..., description="The track file URL")
    duration: int = Field(..., description="The track duration")
    permalink: str = Field(..., description="The track permalink")
    type: Optional[str] = Field(None, description="The track type")
    release_date: Optional[date] = Field(None, description="The track release date")
    track_number: Optional[int] = Field(None, description="The track number")

    class Config:
        orm_mode = True

class TrackCreate(TrackBase):
    pass

class TrackUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The track name")
    file_url: Optional[str] = Field(None, description="The track file URL")
    duration: Optional[int] = Field(None, description="The track duration")
    permalink: Optional[str] = Field(None, description="The track permalink")
    type: Optional[str] = Field(None, description="The track type")
    release_date: Optional[date] = Field(None, description="The track release date")
    track_number: Optional[int] = Field(None, description="The track number")

    class Config:
        orm_mode = True

class TrackResponse(BaseModel):
    status: int
    message: str
    data: Optional[dict] = None

@router.get("/", response_model=TrackResponse)
def get_tracks(
    limit: int = Query(10, description="Limit per page"),
    page: int = Query(1, description="Page number"),
    keyword: str = Query("", description="Search keyword"),
    db: Session = Depends(get_db)
):
    """
    Get all tracks with pagination
    """
    try:
        controller = TrackController()
        result = controller.get_all(limit, page, keyword, db)
        return {
            "status": 200,
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=TrackResponse)
def create_track(track: TrackCreate, db: Session = Depends(get_db)):
    """
    Create a new track
    """
    try:
        controller = TrackController()
        result = controller.store(track.dict(), db)
        return {
            "status": 200,
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=TrackResponse)
def update_track(id: int, track: TrackUpdate, db: Session = Depends(get_db)):
    """
    Update a track
    """
    try:
        controller = TrackController()
        result = controller.update(id, track.dict(exclude_unset=True), db)
        return {
            "status": 200,
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", response_model=TrackResponse)
def delete_track(id: int, db: Session = Depends(get_db)):
    """
    Delete a track
    """
    try:
        controller = TrackController()
        result = controller.destroy(id, db)
        return {
            "status": 200,
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{permalink}", response_model=TrackResponse)
def get_track_by_permalink(permalink: str, db: Session = Depends(get_db)):
    """
    Get a track by permalink
    """
    try:
        controller = TrackController()
        result = controller.get_by_permalink(permalink, db)
        return {
            "status": 200,
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/crawl/{link}", response_model=TrackResponse)
def crawl_track(link: str, db: Session = Depends(get_db)):
    """
    Crawl a track from a link
    """
    try:
        controller = TrackController()
        result = controller.crawl(link, db)
        return {
            "status": 200,
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
