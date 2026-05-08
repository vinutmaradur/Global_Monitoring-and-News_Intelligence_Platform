from Data_Pipeline.utils import load_json, save_json
from Backend.database import SessionLocal
from Data_Pipeline.Earthquake.fetch_earthquake import fetch_earthquakes
from Backend.models import Earthquake

def store_earthquakes():
    db = SessionLocal()
    earthquakes = fetch_earthquakes()

    for eq in earthquakes:
        exists = db.query(Earthquake).filter_by(
            time=eq["time"],
            latitude=eq["latitude"],
            longitude=eq["longitude"]
        ).first()

        if not exists:
            new_eq = Earthquake(**eq)
            db.add(new_eq)

    db.commit()
    db.close()
    print("Earthquake data stored!")

def merge_all():
    news = load_json("data\\raw\\news.json")
    weather = load_json("data\\raw\\weather.json")
    crypto = load_json("data\\raw\\crypto.json")
    earthquake = load_json("data\\raw\\earthquake.json")

    combined = {
        "news": news,
        "weather": weather,
        "crypto": crypto,
        "earthquake": earthquake
    }

    save_json(combined, "data\\raw\\combined.json")
    print("Data merged!")



if __name__ == "__main__":
    merge_all()
    store_earthquakes()   