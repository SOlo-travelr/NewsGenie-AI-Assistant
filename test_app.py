"""Test script for NewsGenie – bypasses API keys with mocks."""

from unittest.mock import patch, MagicMock
from workflow import build_workflow, GraphState


def mock_llm_invoke(messages):
    """Fake LLM that returns deterministic classification/responses."""
    last_content = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])

    # Classification node detection — extract the quoted user query
    if "Classify the following user query" in last_content:
        import re
        match = re.search(r'User query: "(.+?)"', last_content)
        user_query = match.group(1).lower() if match else last_content.lower()

        if user_query in ("hello!", "hi", "hey"):
            return MagicMock(content="TYPE: greeting\nCATEGORY: none")
        elif "news" in user_query or "headline" in user_query:
            return MagicMock(content="TYPE: news\nCATEGORY: technology")
        else:
            return MagicMock(content="TYPE: general\nCATEGORY: none")

    # Response generation node
    return MagicMock(content="This is a mocked NewsGenie response for testing purposes.")


def mock_news_api(*args, **kwargs):
    return {
        "success": True,
        "articles": [
            {
                "title": "AI Breakthrough in 2026",
                "description": "Researchers announce major advancement in AI.",
                "url": "https://example.com/ai-news",
                "source": "TechDaily",
                "published_at": "2026-04-19T10:00:00Z",
            },
            {
                "title": "New Python Release",
                "description": "Python 3.14 brings exciting features.",
                "url": "https://example.com/python",
                "source": "DevNews",
                "published_at": "2026-04-18T08:00:00Z",
            },
        ],
        "error": None,
    }


def mock_web_search(*args, **kwargs):
    return {
        "success": True,
        "results": [
            {
                "title": "What is LangGraph?",
                "content": "LangGraph is a framework for building stateful AI agents.",
                "url": "https://example.com/langgraph",
            }
        ],
        "error": None,
    }


def run_test(name, query, expected_type):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"Query: \"{query}\"")
    print(f"{'='*60}")

    app = build_workflow()
    state: GraphState = {
        "user_query": query,
        "query_type": "",
        "news_category": None,
        "chat_history": [],
        "news_results": "",
        "search_results": "",
        "final_response": "",
    }

    result = app.invoke(state)

    print(f"  Query Type:     {result['query_type']}")
    print(f"  News Category:  {result['news_category']}")
    print(f"  News Results:   {'Yes' if result['news_results'] else 'None'}")
    print(f"  Search Results: {'Yes' if result['search_results'] else 'None'}")
    print(f"  Final Response: {result['final_response'][:100]}...")

    assert result["query_type"] == expected_type, f"Expected '{expected_type}', got '{result['query_type']}'"
    assert result["final_response"], "Final response should not be empty"
    print(f"  RESULT: PASSED ✓")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("  NewsGenie - Component Test Suite (Mocked APIs)")
    print("=" * 60)

    # Patch all external calls
    with (
        patch("workflow.get_llm") as mock_get_llm,
        patch("workflow.fetch_top_headlines", side_effect=mock_news_api),
        patch("workflow.search_news", side_effect=mock_news_api),
        patch("workflow.web_search", side_effect=mock_web_search),
    ):
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke = mock_llm_invoke
        mock_get_llm.return_value = mock_llm_instance

        tests_passed = 0
        tests_failed = 0

        test_cases = [
            ("Greeting Query", "Hello!", "greeting"),
            ("News Query", "Show me the latest technology news", "news"),
            ("General Query", "What is machine learning?", "general"),
        ]

        for name, query, expected in test_cases:
            try:
                run_test(name, query, expected)
                tests_passed += 1
            except Exception as e:
                print(f"  RESULT: FAILED ✗ — {e}")
                tests_failed += 1

    # Test individual modules (no API calls needed)
    print(f"\n{'='*60}")
    print("MODULE IMPORT TESTS")
    print(f"{'='*60}")

    modules = [
        ("config", "config"),
        ("news_api", "news_api"),
        ("web_search", "web_search"),
        ("workflow", "workflow"),
    ]
    for label, mod in modules:
        try:
            __import__(mod)
            print(f"  {label}: OK ✓")
            tests_passed += 1
        except Exception as e:
            print(f"  {label}: FAILED ✗ — {e}")
            tests_failed += 1

    # Test workflow graph compilation
    try:
        wf = build_workflow()
        print(f"  Workflow compile: OK ✓  ({type(wf).__name__})")
        tests_passed += 1
    except Exception as e:
        print(f"  Workflow compile: FAILED ✗ — {e}")
        tests_failed += 1

    # Test news formatting
    from news_api import format_articles
    from web_search import format_search_results

    articles = mock_news_api()["articles"]
    formatted = format_articles(articles)
    assert "AI Breakthrough" in formatted
    print(f"  News formatting: OK ✓")
    tests_passed += 1

    results = mock_web_search()["results"]
    formatted = format_search_results(results)
    assert "LangGraph" in formatted
    print(f"  Search formatting: OK ✓")
    tests_passed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY: {tests_passed} passed, {tests_failed} failed")
    print(f"{'='*60}")
