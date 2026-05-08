from Backend.database import SessionLocal
from Backend.crud import create_article, get_articles

db = SessionLocal()

# 🔹 Create article
create_article(
    db,
    title="AI Revolution",
    content="AI is everywhere",
    url="http://ai.com",
    country_name="India",
    topic_name="Technology"
)

# 🔹 Fetch articles
articles = get_articles(db)

# ✅ ADD HERE
print("Total articles:", len(articles))

# 🔹 Print data
for a in articles:
    print(a.title, a.country.name, a.topic.name)

db.close()