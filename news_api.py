"""News API integration for fetching real-time news articles."""

import requests
from config import NEWS_API_KEY, NEWS_API_BASE_URL


def fetch_top_headlines(category: str = "general", country: str = "us", page_size: int = 5) -> dict:
    """Fetch top headlines from NewsAPI by category.

    Returns a dict with 'success' bool, 'articles' list, and optional 'error' message.
    """
    if not NEWS_API_KEY:
        return {
            "success": False,
            "articles": [],
            "error": "NEWS_API_KEY is not configured. Please set it in your .env file.",
        }

    url = f"{NEWS_API_BASE_URL}/top-headlines"
    params = {
        "category": category,
        "country": country,
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok":
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", "No title"),
                    "description": article.get("description", "No description available"),
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "published_at": article.get("publishedAt", ""),
                })
            return {"success": True, "articles": articles, "error": None}
        else:
            return {
                "success": False,
                "articles": [],
                "error": data.get("message", "Unknown error from NewsAPI"),
            }

    except requests.exceptions.Timeout:
        return {"success": False, "articles": [], "error": "NewsAPI request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "articles": [], "error": "Could not connect to NewsAPI. Check your internet connection."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "articles": [], "error": f"NewsAPI HTTP error: {e}"}
    except Exception as e:
        return {"success": False, "articles": [], "error": f"Unexpected error fetching news: {e}"}


def search_news(query: str, page_size: int = 5) -> dict:
    """Search news articles by keyword query."""
    if not NEWS_API_KEY:
        return {
            "success": False,
            "articles": [],
            "error": "NEWS_API_KEY is not configured. Please set it in your .env file.",
        }

    url = f"{NEWS_API_BASE_URL}/everything"
    params = {
        "q": query,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok":
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", "No title"),
                    "description": article.get("description", "No description available"),
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "published_at": article.get("publishedAt", ""),
                })
            return {"success": True, "articles": articles, "error": None}
        else:
            return {
                "success": False,
                "articles": [],
                "error": data.get("message", "Unknown error from NewsAPI"),
            }

    except requests.exceptions.Timeout:
        return {"success": False, "articles": [], "error": "NewsAPI request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "articles": [], "error": "Could not connect to NewsAPI. Check your internet connection."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "articles": [], "error": f"NewsAPI HTTP error: {e}"}
    except Exception as e:
        return {"success": False, "articles": [], "error": f"Unexpected error searching news: {e}"}


def format_articles(articles: list[dict]) -> str:
    """Format a list of articles into a readable string."""
    if not articles:
        return "No articles found."

    formatted = []
    for i, article in enumerate(articles, 1):
        formatted.append(
            f"**{i}. {article['title']}**\n"
            f"   Source: {article['source']} | Published: {article['published_at'][:10] if article['published_at'] else 'N/A'}\n"
            f"   {article['description']}\n"
            f"   [Read more]({article['url']})"
        )
    return "\n\n".join(formatted)
