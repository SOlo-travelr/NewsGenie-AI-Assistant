"""LangGraph-based workflow for NewsGenie query processing."""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from config import OPENAI_API_KEY, NEWS_CATEGORIES
from news_api import fetch_top_headlines, search_news, format_articles
from web_search import web_search, format_search_results


# ---------------------------------------------------------------------------
# State definition
# ---------------------------------------------------------------------------

class GraphState(TypedDict):
    user_query: str
    query_type: str  # "news", "general", or "greeting"
    news_category: str | None
    chat_history: list
    news_results: str
    search_results: str
    final_response: str


# ---------------------------------------------------------------------------
# LLM instance
# ---------------------------------------------------------------------------

def get_llm():
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured. Please set it in your .env file.")
    return ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.3)


# ---------------------------------------------------------------------------
# Node: Classify Query
# ---------------------------------------------------------------------------

def classify_query(state: GraphState) -> GraphState:
    """Classify the user query as 'news', 'general', or 'greeting'."""
    llm = get_llm()

    classification_prompt = f"""Classify the following user query into exactly one of these categories:
- "news": The user is asking for news, headlines, updates, or current events about a topic.
- "general": The user is asking a general knowledge question, seeking information, or asking for help.
- "greeting": The user is saying hello, hi, or making casual small talk.

User query: "{state['user_query']}"

Also, if the query is about news, identify the most relevant news category from this list:
{NEWS_CATEGORIES}

Respond in this exact format:
TYPE: <news|general|greeting>
CATEGORY: <category or none>"""

    response = llm.invoke([HumanMessage(content=classification_prompt)])
    response_text = response.content.strip()

    query_type = "general"
    news_category = None

    for line in response_text.split("\n"):
        line = line.strip()
        if line.startswith("TYPE:"):
            query_type = line.split(":", 1)[1].strip().lower()
        elif line.startswith("CATEGORY:"):
            cat = line.split(":", 1)[1].strip().lower()
            if cat != "none" and cat in NEWS_CATEGORIES:
                news_category = cat

    state["query_type"] = query_type
    state["news_category"] = news_category
    return state


# ---------------------------------------------------------------------------
# Node: Fetch News
# ---------------------------------------------------------------------------

def fetch_news_node(state: GraphState) -> GraphState:
    """Fetch news articles based on category or search query."""
    category = state.get("news_category")
    user_query = state["user_query"]

    if category:
        result = fetch_top_headlines(category=category)
    else:
        result = search_news(query=user_query)

    if result["success"] and result["articles"]:
        state["news_results"] = format_articles(result["articles"])
    elif result["error"]:
        # Fallback: try web search when news API fails
        state["news_results"] = f"⚠️ News API issue: {result['error']}"
    else:
        state["news_results"] = "No news articles found for this query."

    return state


# ---------------------------------------------------------------------------
# Node: Web Search
# ---------------------------------------------------------------------------

def web_search_node(state: GraphState) -> GraphState:
    """Perform supplementary web search for additional context."""
    result = web_search(query=state["user_query"])

    if result["success"] and result["results"]:
        state["search_results"] = format_search_results(result["results"])
    elif result["error"]:
        state["search_results"] = f"⚠️ Web search issue: {result['error']}"
    else:
        state["search_results"] = ""

    return state


# ---------------------------------------------------------------------------
# Node: Generate Response
# ---------------------------------------------------------------------------

def generate_response(state: GraphState) -> GraphState:
    """Generate the final response using the LLM with gathered context."""
    llm = get_llm()

    system_msg = SystemMessage(content="""You are NewsGenie, an AI-powered information and news assistant.
You help users stay updated with real-time news and answer general queries.
Be concise, informative, and friendly. Use markdown formatting for readability.
When presenting news, include source attribution and links.
If news data is unavailable, acknowledge it and provide what information you can from web search results.""")

    # Build context from gathered information
    context_parts = []

    if state.get("news_results") and state["query_type"] == "news":
        context_parts.append(f"**News Results:**\n{state['news_results']}")

    if state.get("search_results") and state["query_type"] in ("general", "news"):
        context_parts.append(f"**Web Search Results:**\n{state['search_results']}")

    context = "\n\n".join(context_parts)

    if state["query_type"] == "greeting":
        user_content = (
            f"The user said: \"{state['user_query']}\"\n"
            "Respond with a friendly greeting and let them know you can help with news updates "
            "and general queries. Mention the news categories available: technology, business, "
            "sports, science, health, entertainment, general."
        )
    elif context:
        user_content = (
            f"User query: \"{state['user_query']}\"\n\n"
            f"Here is the information I gathered:\n{context}\n\n"
            "Please synthesize this into a helpful, well-formatted response for the user."
        )
    else:
        user_content = (
            f"User query: \"{state['user_query']}\"\n\n"
            "I couldn't fetch external data. Please answer based on your knowledge, "
            "and let the user know that real-time data may not be available right now."
        )

    # Include recent chat history for context continuity
    messages = [system_msg]
    for msg in state.get("chat_history", [])[-6:]:  # last 3 exchanges
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_content))

    response = llm.invoke(messages)
    state["final_response"] = response.content
    return state


# ---------------------------------------------------------------------------
# Routing function
# ---------------------------------------------------------------------------

def route_query(state: GraphState) -> str:
    """Route to the appropriate processing node based on query type."""
    if state["query_type"] == "news":
        return "fetch_news"
    elif state["query_type"] == "general":
        return "web_search"
    else:  # greeting
        return "generate_response"


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def build_workflow() -> StateGraph:
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("classify_query", classify_query)
    workflow.add_node("fetch_news", fetch_news_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generate_response", generate_response)

    # Set entry point
    workflow.set_entry_point("classify_query")

    # Add conditional routing after classification
    workflow.add_conditional_edges(
        "classify_query",
        route_query,
        {
            "fetch_news": "fetch_news",
            "web_search": "web_search",
            "generate_response": "generate_response",
        },
    )

    # After fetching news, also do web search for supplementary info
    workflow.add_edge("fetch_news", "web_search")

    # After web search, generate the final response
    workflow.add_edge("web_search", "generate_response")

    # End after generating response
    workflow.add_edge("generate_response", END)

    return workflow.compile()


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def process_query(user_query: str, chat_history: list | None = None) -> str:
    """Process a user query through the NewsGenie workflow.

    Args:
        user_query: The user's input text.
        chat_history: List of dicts with 'role' and 'content' keys.

    Returns:
        The assistant's response string.
    """
    app = build_workflow()

    initial_state: GraphState = {
        "user_query": user_query,
        "query_type": "",
        "news_category": None,
        "chat_history": chat_history or [],
        "news_results": "",
        "search_results": "",
        "final_response": "",
    }

    try:
        result = app.invoke(initial_state)
        return result["final_response"]
    except ValueError as e:
        return f"⚠️ Configuration Error: {e}"
    except Exception as e:
        return f"⚠️ An error occurred while processing your query: {e}\n\nPlease try again or rephrase your question."
