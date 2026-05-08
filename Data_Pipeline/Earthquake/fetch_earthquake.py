import requests
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from apscheduler.schedulers.background import BackgroundScheduler
import time

# -------------------------------
# ⚙️ POSTGRES CONFIG
# -------------------------------
DB_CONFIG = {
    "host": "localhost",
    "database": "news_db",
    "user": "postgres",
    "password": "Vinut123890"
}

earthquake_api = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
)

# -------------------------------
# 🗄️ INIT DB
# -------------------------------
def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id TEXT PRIMARY KEY,
            location TEXT,
            magnitude FLOAT,
            time TIMESTAMP,
            latitude FLOAT,
            longitude FLOAT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# -------------------------------
# 🌍 FETCH EARTHQUAKES
# -------------------------------
def fetch_earthquakes():
    print("🌍 Fetching latest earthquakes...")

    try:
        response = requests.get(earthquake_api, timeout=5)

        if response.status_code != 200:
            print("❌ API Error:", response.status_code)
            return

        data = response.json()

    except Exception as e:
        print("❌ Request Failed:", e)
        return

    records = []

    for eq in data["features"]:
        try:
            properties = eq["properties"]
            geometry = eq["geometry"]

            if properties["mag"] is None:
                continue

            earthquake_id = eq["id"]

            timestamp_ms = properties["time"]

            readable_time = datetime.utcfromtimestamp(
                timestamp_ms / 1000
            )

            records.append((
                earthquake_id,
                properties["place"],
                properties["mag"],
                readable_time,
                geometry["coordinates"][1],
                geometry["coordinates"][0]
            ))

        except:
            continue

    if not records:
        print("⚠️ No records")
        return

    # -------------------------------
    # 🚀 BULK INSERT
    # -------------------------------
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        execute_values(
            cur,
            """
            INSERT INTO earthquakes
            (id, location, magnitude, time, latitude, longitude)
            VALUES %s
            ON CONFLICT (id) DO NOTHING
            """,
            records
        )

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ Inserted {len(records)} earthquake records")

    except Exception as e:
        print("❌ DB Error:", e)


# -------------------------------
# ⏱️ AUTO REFRESH
# -------------------------------
init_db()

scheduler = BackgroundScheduler()

# 🔥 refresh every 5 minutes
scheduler.add_job(fetch_earthquakes, 'interval', minutes=5)

scheduler.start()

# Run immediately once
fetch_earthquakes()

print("⚡ Earthquake pipeline running...")

# Keep script alive
while True:
    time.sleep(60)