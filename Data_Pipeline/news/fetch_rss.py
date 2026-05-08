import feedparser
import requests
import spacy
import time
import psycopg2
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

nlp = spacy.load("en_core_web_sm")

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://rss.cnn.com/rss/edition.rss",
    "https://feeds.reuters.com/reuters/worldNews",
]

DB_CONFIG = {
    "host": "localhost",
    "database": "news_db",
    "user": "postgres",
    "password": "Vinut123890"
}

# -----------------------------
# DB INIT
# -----------------------------
def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rss_news (
            url TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            source TEXT,
            place TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            published_at TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# -----------------------------
# GEO (simple + safe fallback)
# -----------------------------
def get_coords(place):
    try:
        res = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place, "format": "json", "limit": 1},
            headers={"User-Agent": "rss-globe"},
            timeout=5
        )

        if res.status_code == 200:
            data = res.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except:
        pass

    return None, None


# -----------------------------
# FETCH RSS
# -----------------------------
def fetch_rss():
    print("📰 Fetching RSS...")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:30]:
            try:
                url = entry.get("link")
                title = entry.get("title", "")
                desc = entry.get("summary", "")

                doc = nlp(title)
                place = None

                for ent in doc.ents:
                    if ent.label_ == "GPE":
                        place = ent.text
                        break

                if not place:
                    continue

                lat, lon = get_coords(place)

                published = entry.get("published", "")
                try:
                    published_dt = datetime.strptime(
                        published[:25], "%a, %d %b %Y %H:%M:%S"
                    )
                except:
                    published_dt = datetime.utcnow()

                cur.execute("""
                    INSERT INTO rss_news
                    (url, title, description, source, place, latitude, longitude, published_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (url) DO NOTHING
                """, (
                    url,
                    title,
                    desc,
                    feed.feed.get("title", "RSS"),
                    place,
                    lat,
                    lon,
                    published_dt
                ))

                inserted += 1

            except:
                continue

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ RSS inserted: {inserted}")


# -----------------------------
# SCHEDULER
# -----------------------------
init_db()

scheduler = BackgroundScheduler()

# 🔥 Choose ONE:
scheduler.add_job(fetch_rss, "interval", minutes=15)   # recommended
# scheduler.add_job(fetch_rss, "interval", hours=1)    # slower option

scheduler.start()

fetch_rss()

print("⚡ RSS pipeline running...")

while True:
    time.sleep(60)