from Backend.models import NewsArticle, Country, Topic , Earthquake


# 🔹 Create Article (using names instead of IDs)
def create_article(db, title, content, url, country_name, topic_name):
    try:
        # Get country
        country = db.query(Country).filter_by(name=country_name).first()
        if not country:
            raise ValueError(f"Country '{country_name}' not found")

        # Get topic
        topic = db.query(Topic).filter_by(name=topic_name).first()
        if not topic:
            raise ValueError(f"Topic '{topic_name}' not found")

        # Create article
        article = NewsArticle(
            title=title,
            content=content,
            url=url,
            country_id=country.id,
            topic_id=topic.id
        )

        db.add(article)
        db.commit()
        db.refresh(article)

        return article

    except Exception as e:
        db.rollback()
        print("❌ Error creating article:", e)
        return None


def add_earthquake(db, eq_data):
    earthquake = Earthquake(**eq_data)
    db.add(earthquake)
    db.commit()
    db.refresh(earthquake)
    return earthquake


# 🔹 Get All Articles
def get_articles(db):
    return db.query(NewsArticle).all()


# 🔹 Get Articles by Country
def get_articles_by_country(db, country_name):
    return (
        db.query(NewsArticle)
        .join(Country)
        .filter(Country.name == country_name)
        .all()
    )


# 🔹 Get Articles by Topic
def get_articles_by_topic(db, topic_name):
    return (
        db.query(NewsArticle)
        .join(Topic)
        .filter(Topic.name == topic_name)
        .all()
    )


# 🔹 Delete Article
def delete_article(db, article_id):
    article = db.query(NewsArticle).filter_by(id=article_id).first()

    if not article:
        print("❌ Article not found")
        return False

    db.delete(article)
    db.commit()
    return True