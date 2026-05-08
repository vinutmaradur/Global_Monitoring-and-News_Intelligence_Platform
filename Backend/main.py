from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.routers import news, earthquake, weather, countries
from Backend.schemas import EarthquakeSchema
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(earthquake.router)
app.include_router(weather.router)
app.include_router(countries.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "World Monitor Backend Running"}

