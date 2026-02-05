from fastapi import APIRouter
import requests

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

GNEWS_API_KEY = "8d89288096813d06aecf58f314d9fb7d"

@router.get("")
def get_cyber_news():
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": "cyber fraud india",
        "lang": "en",
        "country": "in",
        "max": 5,
        "apikey": GNEWS_API_KEY
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        articles = []
        for item in data.get("articles", []):
            articles.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "source": item.get("source", {}).get("name")
            })

        return {
            "status": "ok",
            "articles": articles
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "News temporarily unavailable"
        }
