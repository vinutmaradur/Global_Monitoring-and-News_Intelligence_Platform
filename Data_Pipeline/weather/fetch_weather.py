import requests
import json
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from apscheduler.schedulers.background import BackgroundScheduler

from Data_Pipeline.config import WEATHER_API_KEY


# --------------------------------
# ⚙️ POSTGRES CONFIG
# --------------------------------
DB_CONFIG = {
    "host": "localhost",
    "database": "news_db",
    "user": "postgres",
    "password": "Vinut123890"
}


# --------------------------------
# 🌍 TARGET CITIES
# --------------------------------
TARGET_CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Hyderabad",
    "Chennai", "Kolkata", "Pune", "Ahmedabad",

    "New York", "Los Angeles", "Chicago",
    "Houston", "Phoenix", "San Francisco",

    "London", "Manchester", "Birmingham",
    "Liverpool",

    "Toronto", "Vancouver", "Montreal",

    "Sydney", "Melbourne", "Brisbane",

    "Berlin", "Munich", "Hamburg",

    "Paris", "Lyon",

    "Tokyo", "Osaka",

    "Dubai", "Abu Dhabi",

    "Singapore"
]


# --------------------------------
# ✅ FIXED COORDS
# --------------------------------
FIXED_COORDS = {
    "Hyderabad": (17.3850, 78.4867),
}


# --------------------------------
# 🗄️ INIT DB
# --------------------------------
def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT PRIMARY KEY,
            temperature FLOAT,
            weather TEXT,
            humidity INT,
            latitude FLOAT,
            longitude FLOAT,
            updated_at TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# --------------------------------
# 📂 LOAD CITY DATA
# --------------------------------
def load_cities():
    with open("data/raw/city.list.json", "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------
# 🌦️ FETCH WEATHER
# --------------------------------
def fetch_weather(lat, lon, city_name):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={WEATHER_API_KEY}"
        f"&units=metric"
    )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("cod") != 200:
            return None

        return (
            city_name,
            data["main"]["temp"],
            data["main"]["humidity"],
            data["weather"][0]["description"],
            datetime.utcnow(),
            lat,
            lon,
            data["sys"]["country"]
        )

    except:
        return None


# --------------------------------
# 🚀 MAIN PIPELINE
# --------------------------------
def update_weather():

    print("🌤️ Fetching weather data...")

    cities_data = load_cities()

    records = []
    found_cities = set()

    for city in cities_data:

        name = city["name"]

        # ✅ only target cities
        if name not in TARGET_CITIES:
            continue

        # ✅ avoid duplicates
        if name in found_cities:
            continue

        found_cities.add(name)

        lat = city["coord"]["lat"]
        lon = city["coord"]["lon"]

        # ✅ override bad coords
        if name in FIXED_COORDS:
            lat, lon = FIXED_COORDS[name]

        result = fetch_weather(lat, lon, name)

        if result:
            records.append(result)
            print(f"✅ {name} updated")

        # ⚡ avoid API spam
        time.sleep(1)

    if not records:
        print("⚠️ No weather data")
        return

    # --------------------------------
    # 💾 SAVE TO POSTGRES
    # --------------------------------
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        execute_values(
             cur,
            """
            INSERT INTO weather
            (city, temperature, humidity, description, timestamp, lat, lon, country)
         VALUES %s

        ON CONFLICT (city)
        DO UPDATE SET
        temperature = EXCLUDED.temperature,
        humidity = EXCLUDED.humidity,
        description = EXCLUDED.description,
        timestamp = EXCLUDED.timestamp,
        lat = EXCLUDED.lat,
        lon = EXCLUDED.lon,
        country = EXCLUDED.country
    """,
    records
        )

        conn.commit()

        cur.close()
        conn.close()

        print(f"🔥 Updated weather for {len(records)} cities")

    except Exception as e:
        print("❌ DB Error:", e)


# --------------------------------
# ⏱️ SCHEDULER
# --------------------------------
init_db()

scheduler = BackgroundScheduler()

# ✅ Refresh every 15 minutes
scheduler.add_job(update_weather, 'interval', minutes=15)

scheduler.start()

# ✅ Run immediately once
update_weather()

print("⚡ Weather pipeline running...")


# --------------------------------
# 🔄 KEEP ALIVE
# --------------------------------
while True:
    time.sleep(60)