import requests
from Data_Pipeline.config import NEWS_API_KEY
from Data_Pipeline.utils import save_json

URL = f"https://newsapi.org/v2/top-headlines"

def fetch_news():
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "category": "technology",
        "pageSize": 10
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Error:", response.status_code)
        return None

    articles = data.get("articles", [])

    clean_data = []
    for article in articles:
        clean_data.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article["source"]["name"],
            "published_at": article.get("publishedAt"),
            "url": article.get("url")
        })
        
    save_json(clean_data, "data\\raw\\news.json")
    print("News saved!")

if __name__ == "__main__":
    fetch_news()
