from Backend.database import SessionLocal
from Backend.models import Weather, Country
import json
from datetime import datetime

db = SessionLocal()

# 🔹 City → Country mapping
CITY_COUNTRY_MAP = {
    "Delhi": "India", "Mumbai": "India", "Bangalore": "India",
    "Hyderabad": "India", "Chennai": "India", "Kolkata": "India",
    "Pune": "India", "Ahmedabad": "India",

    "London": "United Kingdom", "Manchester": "United Kingdom",
    "Liverpool": "United Kingdom", "Birmingham": "United Kingdom",

    "New York": "United States", "Los Angeles": "United States",
    "Chicago": "United States", "Houston": "United States",
    "Phoenix": "United States", "San Francisco": "United States",

    "Toronto": "Canada", "Vancouver": "Canada",

    "Sydney": "Australia", "Melbourne": "Australia", "Brisbane": "Australia",

    "Berlin": "Germany", "Munich": "Germany", "Hamburg": "Germany",

    "Paris": "France", "Lyon": "France",

    "Tokyo": "Japan", "Osaka": "Japan",

    "Dubai": "UAE", "Abu Dhabi": "UAE",

    "Singapore": "Singapore"
}

try:
    # 🔹 Load weather JSON
    with open("data/raw/weather.json", "r", encoding="utf-8") as f:
        weather_data = json.load(f)

    inserted = 0

    for item in weather_data:
        city = item["city"]
        country_name = CITY_COUNTRY_MAP.get(city)

        if not country_name:
            continue

        # 🔹 Get country from DB
        country = db.query(Country).filter_by(name=country_name).first()
        if not country:
            continue

        # 🔹 Insert weather
        weather = Weather(
            city=city,
            temperature=item["temperature"],
            humidity=item.get("humidity"),
            description=item["weather"],
            lat=item["lat"],        
            lon=item["lon"],
            timestamp=datetime.utcnow(),
            country_id=country.id
        )

        db.add(weather)
        inserted += 1

    db.commit()
    print(f"✅ {inserted} weather records inserted")

except Exception as e:
    print("❌ Error:", e)
    db.rollback()

finally:
    db.close()