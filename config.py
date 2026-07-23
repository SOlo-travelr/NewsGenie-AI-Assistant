"""Configuration and environment variable management for NewsGenie."""

import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key(key_name: str) -> str | None:
    """Retrieve an API key from environment variables."""
    return os.getenv(key_name)


OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")
NEWS_API_KEY = get_api_key("NEWS_API_KEY")
TAVILY_API_KEY = get_api_key("TAVILY_API_KEY")

NEWS_CATEGORIES = [
    "technology",
    "business",
    "sports",
    "science",
    "health",
    "entertainment",
    "general",
]

NEWS_API_BASE_URL = "https://newsapi.org/v2"
