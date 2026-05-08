from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.models import Weather
from Backend.schemas import WeatherSchema
from typing import List, Optional

router = APIRouter(prefix="/weather")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[WeatherSchema])
def get_weather(
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Weather)

    if city:
        query = query.filter(Weather.city == city)

    return query.all()