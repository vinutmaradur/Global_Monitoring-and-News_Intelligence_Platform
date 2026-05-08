from Backend.database import SessionLocal
from Backend.models import Country

db = SessionLocal()

new_country = Country(name="India")

db.add(new_country)
db.commit()

print("Inserted successfully!")