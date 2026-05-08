from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Backend.models import NewsArticle, RssNews
from Backend.database import SessionLocal
from typing import List, Optional
from Backend.schemas import NewsSchema, RssNewsSchema
from datetime import datetime, timedelta , timezone

router = APIRouter()


# -------------------------------
# DB Dependency
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# 🔥 UNIFIED TIME PARSER (FIXED)
# -------------------------------
def parse_time_filter(value: Optional[str]):
    if not value:
        return None

    now = datetime.now(timezone.utc)

    try:
        value = str(value).lower().strip()

        # 24h format
        if value.endswith("h"):
            return now - timedelta(hours=int(value[:-1]))

        # 7d format
        if value.endswith("d"):
            return now - timedelta(days=int(value[:-1]))

        # raw number → assume hours
        return now - timedelta(hours=int(value))

    except:
        return None


# -------------------------------
# 🔹 NEWS
# -------------------------------
@router.get("/news", response_model=List[NewsSchema])
def get_news(
    country_id: Optional[int] = None,
    last_hour: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(NewsArticle)

    if country_id:
        query = query.filter(NewsArticle.country_id == country_id)

    threshold = parse_time_filter(last_hour)

    if threshold:
        query = query.filter(NewsArticle.published_at >= threshold)

    return query.order_by(NewsArticle.published_at.desc()).all()

# -------------------------------
# 🔹 RSS NEWS
# -------------------------------
@router.get("/rss", response_model=List[RssNewsSchema])
def get_rss_news(
    place: Optional[str] = None,
    source: Optional[str] = None,
    last_hour: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(RssNews)

    if place:
        query = query.filter(RssNews.place.ilike(f"%{place}%"))

    if source:
        query = query.filter(RssNews.source.ilike(f"%{source}%"))

    threshold = parse_time_filter(last_hour)

    if threshold:
        query = query.filter(RssNews.published_at >= threshold)

    return query.order_by(RssNews.published_at.desc()).all()