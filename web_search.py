"""Web search tool integration using Tavily for supplementary information."""

from tavily import TavilyClient
from config import TAVILY_API_KEY


def web_search(query: str, max_results: int = 3) -> dict:
    """Perform a web search using the Tavily API.

    Returns a dict with 'success' bool, 'results' list, and optional 'error'.
    """
    if not TAVILY_API_KEY:
        return {
            "success": False,
            "results": [],
            "error": "TAVILY_API_KEY is not configured. Please set it in your .env file.",
        }

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query=query, max_results=max_results)

        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title", "No title"),
                "content": result.get("content", ""),
                "url": result.get("url", ""),
            })

        return {"success": True, "results": results, "error": None}

    except Exception as e:
        return {"success": False, "results": [], "error": f"Web search error: {e}"}


def format_search_results(results: list[dict]) -> str:
    """Format web search results into a readable string."""
    if not results:
        return "No web search results found."

    formatted = []
    for i, result in enumerate(results, 1):
        snippet = result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"]
        formatted.append(
            f"**{i}. {result['title']}**\n"
            f"   {snippet}\n"
            f"   [Source]({result['url']})"
        )
    return "\n\n".join(formatted)
