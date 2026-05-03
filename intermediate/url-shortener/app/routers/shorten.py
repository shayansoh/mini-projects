from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import ShortenURLRequest, URLResponse, URLStatsResponse
from app.service import URLService

router = APIRouter(prefix="/shorten", tags=["shorten"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(db: Session = Depends(get_db)) -> URLService:
    return URLService(db)

@router.post("", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    request: ShortenURLRequest,
    service: URLService = Depends(get_service)
):
    return service.create_short_url(str(request.url))

@router.get("/{short_code}", response_model=URLResponse)
def get_short_url(
    short_code: str,
    service: URLService = Depends(get_service)
):
    return service.get_short_url(short_code)

@router.put("/{short_code}", response_model=URLResponse)
def update_short_url(
    short_code: str,
    request: ShortenURLRequest,
    service: URLService = Depends(get_service)
):
    return service.update_short_url(short_code, str(request.url))

@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_short_url(
    short_code: str,
    service: URLService = Depends(get_service)
):
    service.delete_short_url(short_code)

@router.get("/{short_code}/stats", response_model=URLStatsResponse)
def get_stats(
    short_code: str,
    service: URLService = Depends(get_service)
):
    return service.get_stats(short_code)