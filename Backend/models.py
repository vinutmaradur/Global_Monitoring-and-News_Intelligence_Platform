from sqlalchemy import Column, DateTime, Integer, String , Float, BigInteger , Text
from Backend.database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    source = Column(String)
    published_at = Column(DateTime(timezone=True))

    country_id = Column(Integer, ForeignKey("countries.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))

    country = relationship("Country")
    topic = relationship("Topic")


class RssNews(Base):
    __tablename__ = "rss_news"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(Text)
    url = Column(String, unique=True)

    source = Column(String)
    place = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    published_at = Column(DateTime(timezone=True))

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime(timezone=True))

    lat = Column(Float)
    lon = Column(Float)

    
    country = Column(String)
    
class Earthquake(Base):
    __tablename__ = "earthquakes"

    id = Column(Integer, primary_key=True)
    magnitude = Column(Float)
    location = Column(String)
    time = Column(DateTime(timezone=True))
    latitude = Column(Float)
    longitude = Column(Float)