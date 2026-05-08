from Backend.database import engine
from Backend.models import Base , Earthquake , Weather , Country , Topic  , NewsArticle

print("Creating tables...")

print("Tables detected:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("Done!")