"""NewsGenie – AI-Powered Information and News Assistant (Streamlit App)."""

import streamlit as st
from workflow import process_query
from news_api import fetch_top_headlines, format_articles
from config import NEWS_CATEGORIES, OPENAI_API_KEY, NEWS_API_KEY, TAVILY_API_KEY

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="NewsGenie – AI News Assistant",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom styling
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    .main-header { text-align: center; padding: 1rem 0; }
    .category-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    .stChatMessage { max-width: 100%; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("🧞 NewsGenie")
    st.markdown("*Your AI-powered news & information assistant*")
    st.divider()

    # --- API key status ---
    st.subheader("🔑 API Status")
    st.markdown(
        f"- OpenAI: {'✅ Connected' if OPENAI_API_KEY else '❌ Missing'}\n"
        f"- NewsAPI: {'✅ Connected' if NEWS_API_KEY else '❌ Missing'}\n"
        f"- Tavily: {'✅ Connected' if TAVILY_API_KEY else '❌ Missing'}"
    )
    st.divider()

    # --- News category selector ---
    st.subheader("📰 News Categories")
    st.caption("Select a category to fetch the latest headlines.")

    category_icons = {
        "technology": "💻", "business": "💼", "sports": "⚽",
        "science": "🔬", "health": "🏥", "entertainment": "🎬", "general": "📰",
    }

    for cat in NEWS_CATEGORIES:
        icon = category_icons.get(cat, "📄")
        if st.button(f"{icon} {cat.capitalize()}", key=f"cat_{cat}", use_container_width=True):
            st.session_state.selected_category = cat

    st.divider()

    # --- Clear conversation ---
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_category = None
        st.rerun()

    st.divider()
    st.caption("Built with LangGraph, OpenAI, NewsAPI & Tavily")

# ---------------------------------------------------------------------------
# Main content area
# ---------------------------------------------------------------------------

st.markdown("<h1 class='main-header'>🧞 NewsGenie</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:grey;'>"
    "Ask me anything or select a news category from the sidebar!</p>",
    unsafe_allow_html=True,
)

# --- Handle category selection ---
if st.session_state.selected_category:
    cat = st.session_state.selected_category
    icon = category_icons.get(cat, "📄")
    cat_query = f"Show me the latest {cat} news"

    # Add as user message
    st.session_state.messages.append({"role": "user", "content": cat_query})

    # Fetch news directly for the category
    with st.spinner(f"Fetching {cat} headlines..."):
        result = fetch_top_headlines(category=cat)
        if result["success"] and result["articles"]:
            response = f"{icon} **Latest {cat.capitalize()} Headlines:**\n\n{format_articles(result['articles'])}"
        elif result["error"]:
            # Fallback: use the workflow which will try web search
            response = process_query(cat_query, st.session_state.messages)
        else:
            response = f"No {cat} news found at the moment. Please try again later."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.selected_category = None
    st.rerun()

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat input ---
if user_input := st.chat_input("Ask NewsGenie anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response through the LangGraph workflow
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_query(user_input, st.session_state.messages)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
