from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.models import Country
from Backend.schemas import CountrySchema
from typing import List, Optional

router = APIRouter(prefix="/countries")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CountrySchema])
def get_countries(
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Country)

    if name:
        query = query.filter(Country.name.ilike(f"%{name}%"))

    return query.all()