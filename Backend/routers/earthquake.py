from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.models import Earthquake
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/earthquakes")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_earthquakes(
    place: Optional[str] = None,
    last_hour: int = Query(24),
    db: Session = Depends(get_db)
):
    query = db.query(Earthquake)

    # 🔍 Filter by location
    if place:
        query = query.filter(Earthquake.location.ilike(f"%{place}%"))

    # 🔥 IMPORTANT: DB-side time filter (NO timezone bugs)
    cutoff = datetime.utcnow() - timedelta(hours=last_hour)
    query = query.filter(Earthquake.time >= cutoff)

    results = query.order_by(Earthquake.time.desc()).all()

    print("last_hour:", last_hour, "count:", len(results))

    return [
        {
            "id": eq.id,
            "place": eq.location,
            "magnitude": eq.magnitude,
            "time": eq.time.strftime("%Y-%m-%d %H:%M:%S"),
            "lat": eq.latitude,
            "lon": eq.longitude
        }
        for eq in results
    ]