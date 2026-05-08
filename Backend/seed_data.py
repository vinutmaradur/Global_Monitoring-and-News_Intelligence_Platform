from Backend.database import SessionLocal
from Backend.models import Country, Topic, NewsArticle
import json

db = SessionLocal()

try:
    # 🔹 1. Insert Countries
    countries = ["India",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "France",
    "China",
    "Japan",
    "Russia",
    "Brazil",
    "South Korea",
    "Italy",
    "Spain",
    "Netherlands",
    "Singapore",
    "UAE",
    "South Africa",
    "New Zealand",
    "Saudi Arabia"]

    for c in countries:
        existing = db.query(Country).filter_by(name=c).first()
        if not existing:
            db.add(Country(name=c))

    # 🔹 2. Insert Topics
    topics = ["Politics",
    "Technology",
    "Sports",
    "Business",
    "Health",
    "Science",
    "Entertainment",
    "World",
    "Education",
    "Environment",
    "Economy",
    "Finance",
    "Cybersecurity",
    "AI & Machine Learning",
    "Startups"]

    for t in topics:
        existing = db.query(Topic).filter_by(name=t).first()
        if not existing:
            db.add(Topic(name=t))

    db.commit()
    print("✅ Seed data inserted (no duplicates)")

    # 🔹 3. Get IDs dynamically (NO hardcoding)
    india = db.query(Country).filter_by(name="India").first()
    tech = db.query(Topic).filter_by(name="Technology").first()

    # 🔹 4. Insert ONE sample article (optional)
    existing_article = db.query(NewsArticle).filter_by(
        title="AI is growing fast"
    ).first()

    if not existing_article:
        article = NewsArticle(
            title="AI is growing fast",
            content="AI is transforming the world...",
            url="http://example.com",
            country_id=india.id,
            topic_id=tech.id
        )
        db.add(article)
        db.commit()
        print("✅ Sample article inserted")

    # 🔹 5. Load JSON file
    with open("data/raw/news.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    inserted_count = 0

    # 🔹 6. Insert JSON news (avoid duplicates using URL)
    for item in data:
        exists = db.query(NewsArticle).filter_by(
            url=item.get("url")
        ).first()

        if not exists:
            news = NewsArticle(
                title=item.get("title"),
                content=item.get("description"),
                url=item.get("url"),
                source=item.get("source"),
                published_at=item.get("published_at"),
                country_id=india.id,
                topic_id=tech.id
            )
            db.add(news)
            inserted_count += 1

    db.commit()
    print(f"✅ {inserted_count} new articles inserted from JSON")

    # 🔹 7. Fetch & display
    articles = db.query(NewsArticle).all()

    print("\n📊 Articles:\n")
    for a in articles:
        print(a.title, "|", a.country.name, "|", a.topic.name)

except Exception as e:
    print("❌ Error:", e)
    db.rollback()

finally:
    db.close()

