from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String , Text

class CountrySchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
        
class NewsSchema(BaseModel):
    id: int
    title: str
    content: str
    url: str
    source: str
    published_at: datetime
    country_id: int
    topic_id: int

    model_config = ConfigDict(from_attributes=True)

class WeatherSchema(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: float
    description: str
    timestamp: datetime
    country: str | None = None
    lat: float
    lon: float

    model_config = ConfigDict(from_attributes=True)


class RssNewsSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    url: str
    source: Optional[str] = None
    place: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class EarthquakeSchema(BaseModel):
    id: int
    magnitude: float
    location: str
    time: datetime
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)