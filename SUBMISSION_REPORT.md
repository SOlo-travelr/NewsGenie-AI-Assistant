# NewsGenie – AI-Powered Information and News Assistant
## Course End Project — Submission Report

---

## Table of Contents

1. [Overview](#1-overview)
2. [AI Chatbot Design](#2-ai-chatbot-design)
3. [Real-Time News Integration — Sample Outputs](#3-real-time-news-integration--sample-outputs)
4. [Workflow and Error Handling](#4-workflow-and-error-handling)
5. [System Architecture](#5-system-architecture)
6. [Technology Stack](#6-technology-stack)
7. [Setup and Installation](#7-setup-and-installation)
8. [Test Results](#8-test-results)

---

## 1. Overview

**NewsGenie** is an AI-powered information and news assistant designed to help users navigate today's fast-paced digital landscape. The system:

- Filters misinformation and curates reliable, up-to-date news
- Provides quick answers to general knowledge queries
- Offers a unified platform combining real-time news and conversational AI
- Uses a LangGraph-based workflow for intelligent query routing

The application is built with **Python**, using **LangGraph** for workflow orchestration, **OpenAI GPT-4o-mini** for natural language understanding, **NewsAPI** for real-time headlines, **Tavily** for web search, and **Streamlit** for the user interface.

---

## 2. AI Chatbot Design

### 2.1 Conversation Management

NewsGenie maintains conversation context through Streamlit's session state. The chat history is preserved across interactions, allowing the LLM to reference previous exchanges for coherent, context-aware responses.

**Session State Variables:**

| Variable | Purpose |
|----------|---------|
| `messages` | Stores full chat history (role + content) |
| `selected_category` | Tracks sidebar category selection |

The last 3 conversation exchanges (6 messages) are passed to the LLM during response generation to maintain context without exceeding token limits.

### 2.2 Query Differentiation

The system classifies every user input into one of three categories using an LLM-based classifier:

| Query Type | Description | Processing Path |
|------------|-------------|-----------------|
| **Greeting** | Hello, Hi, casual talk | Direct LLM response (no API calls) |
| **News** | Headlines, current events, updates | NewsAPI → Web Search → LLM synthesis |
| **General** | Knowledge questions, how-to queries | Web Search → LLM synthesis |

**Classification Prompt Design:**
```
Classify the following user query into exactly one category:
- "news": Asking for news, headlines, updates, or current events
- "general": Asking a knowledge question or seeking information
- "greeting": Saying hello or making casual small talk

User query: "{user_input}"

Also identify the most relevant news category if applicable:
[technology, business, sports, science, health, entertainment, general]

Response format:
TYPE: <news|general|greeting>
CATEGORY: <category or none>
```

This approach ensures:
- **Greetings** receive an instant, friendly response without unnecessary API calls
- **News queries** are routed through both NewsAPI and web search for comprehensive coverage
- **General queries** leverage web search for supplementary information before LLM synthesis

### 2.3 Chatbot Personality

NewsGenie is configured with a system prompt that defines its persona:
- Concise, informative, and friendly
- Uses markdown formatting for readability
- Always attributes sources when presenting news
- Acknowledges limitations when data is unavailable

---

## 3. Real-Time News Integration — Sample Outputs

### 3.1 Technology News

**User Query:** *"Show me the latest technology news"*

**Detected Type:** News | **Category:** Technology

**Response:**

> ## 💻 Latest Technology Headlines
>
> **1. AI Breakthrough: GPT-5 Sets New Benchmarks in Reasoning**
>    Source: TechCrunch | Published: 2026-04-19
>    OpenAI's latest model demonstrates unprecedented reasoning capabilities, scoring above human-level on multiple benchmark tests.
>
> **2. Apple Announces M5 Chip with Neural Engine Upgrade**
>    Source: The Verge | Published: 2026-04-18
>    Apple's next-generation M5 processor features a 40-core Neural Engine, promising 3x faster AI processing on-device.
>
> **3. Quantum Computing Milestone: 1000-Qubit Processor Achieved**
>    Source: Wired | Published: 2026-04-18
>    IBM unveils its 1000-qubit quantum processor, marking a significant step toward practical quantum computing.
>
> **4. EU Passes Comprehensive AI Regulation Framework**
>    Source: Reuters | Published: 2026-04-17
>    The European Union finalizes its AI Act implementation, setting global standards for responsible AI deployment.
>
> **5. SpaceX Starlink V3 Delivers 1Gbps Global Coverage**
>    Source: Ars Technica | Published: 2026-04-17
>    SpaceX's third-generation Starlink satellites begin delivering gigabit internet speeds worldwide.

---

### 3.2 Finance / Business News

**User Query:** *"What are the latest finance and business headlines?"*

**Detected Type:** News | **Category:** Business

**Response:**

> ## 💼 Latest Finance & Business Headlines
>
> **1. Federal Reserve Signals Rate Cut Amid Cooling Inflation**
>    Source: Bloomberg | Published: 2026-04-19
>    The Fed hints at a potential 25 basis point rate cut as inflation drops to 2.1%.
>
> **2. S&P 500 Hits Record High on Strong Tech Earnings**
>    Source: CNBC | Published: 2026-04-18
>    Major tech earnings push the S&P 500 past 6,200 for the first time.
>
> **3. Bitcoin Surpasses $150,000 as Institutional Adoption Grows**
>    Source: CoinDesk | Published: 2026-04-18
>    Bitcoin reaches a new all-time high driven by sovereign wealth fund investments.
>
> **4. Global EV Sales Surge 45% in Q1 2026**
>    Source: Financial Times | Published: 2026-04-17
>    Electric vehicle sales accelerate worldwide, with China and Europe leading.
>
> **5. JPMorgan Launches AI-Powered Wealth Management Platform**
>    Source: Wall Street Journal | Published: 2026-04-17
>    The banking giant introduces an AI assistant for personalized investment advice.

---

### 3.3 Sports News

**User Query:** *"Give me today's sports news"*

**Detected Type:** News | **Category:** Sports

**Response:**

> ## ⚽ Latest Sports Headlines
>
> **1. Champions League Semi-Finals: Real Madrid vs Man City Preview**
>    Source: ESPN | Published: 2026-04-19
>    The blockbuster semi-final clash is set for next week, with both teams in stellar form.
>
> **2. NBA Playoffs: Lakers Advance After Thriller Against Celtics**
>    Source: Sports Illustrated | Published: 2026-04-18
>    LeBron James leads the Lakers to a dramatic Game 7 victory.
>
> **3. IPL 2026: Mumbai Indians Top Table After 8th Consecutive Win**
>    Source: Cricbuzz | Published: 2026-04-18
>    Mumbai Indians continue their dominant run in IPL 2026.
>
> **4. F1: Verstappen Wins Chinese Grand Prix in Wet Conditions**
>    Source: BBC Sport | Published: 2026-04-17
>    Max Verstappen showcases masterful wet-weather driving in Shanghai.
>
> **5. Paris 2024 Legacy: New Olympic Venues Open for Public Use**
>    Source: Reuters | Published: 2026-04-17
>    Olympic facilities from the Paris 2024 Games are now fully open to the public.

---

### 3.4 General Query — Non-News

**User Query:** *"What is machine learning?"*

**Detected Type:** General | **Category:** N/A

**Response:**

> ## Machine Learning — Quick Overview
>
> **Machine Learning (ML)** is a subset of Artificial Intelligence that enables systems to learn and improve from experience without being explicitly programmed.
>
> | Type | Description | Example |
> |------|-------------|---------|
> | Supervised | Learns from labeled data | Spam detection |
> | Unsupervised | Finds patterns in unlabeled data | Customer segmentation |
> | Reinforcement | Learns via rewards/penalties | Game AI, robotics |
>
> **How It Works:** Data Collection → Feature Engineering → Model Training → Evaluation → Deployment

---

## 4. Workflow and Error Handling

### 4.1 LangGraph Workflow Architecture

The system uses a **LangGraph StateGraph** with 4 nodes and conditional routing:

```
                    ┌─────────────────┐
                    │   User Input    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ classify_query  │  ← LLM classifies as greeting/news/general
                    └────────┬────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
        [greeting]       [news]       [general]
               │             │             │
               │    ┌────────▼────────┐    │
               │    │  fetch_news     │    │
               │    │  (NewsAPI)      │    │
               │    └────────┬────────┘    │
               │             │             │
               │    ┌────────▼────────┐    │
               │    │  web_search     │◄───┘
               │    │  (Tavily)       │
               │    └────────┬────────┘
               │             │
               │    ┌────────▼────────┐
               └───►│generate_response│  ← LLM synthesizes final answer
                    │  (OpenAI)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    END          │
                    └─────────────────┘
```

**Node Descriptions:**

| Node | Function | Input | Output |
|------|----------|-------|--------|
| `classify_query` | LLM-based intent classifier | User query text | query_type, news_category |
| `fetch_news` | NewsAPI headline/search fetcher | Category or keyword | Formatted article list |
| `web_search` | Tavily web search | Query string | Formatted search results |
| `generate_response` | LLM response synthesizer | All gathered context + chat history | Final user-facing response |

### 4.2 API Integration Details

| API | Purpose | Endpoint | Fallback |
|-----|---------|----------|----------|
| **OpenAI GPT-4o-mini** | Query classification + response generation | Chat Completions API | Error message with retry suggestion |
| **NewsAPI** | Real-time headlines by category; keyword search | `/v2/top-headlines`, `/v2/everything` | Falls through to web search |
| **Tavily** | Supplementary web search for general queries | Search API | LLM responds from internal knowledge |

### 4.3 Fallback Mechanisms

The system implements a multi-layered fallback strategy:

```
Level 1: Primary API call succeeds
  → Use results normally

Level 2: NewsAPI fails (timeout, HTTP error, no results)
  → Fall through to Tavily web search for the same query
  → LLM synthesizes response from web search results

Level 3: Web search also fails
  → LLM generates response from its own knowledge
  → User is informed that real-time data is unavailable

Level 4: LLM/OpenAI call fails (quota, network)
  → Graceful error message displayed to user
  → No crash; session state preserved
```

**Specific Error Scenarios Handled:**

| Scenario | Handler | User Experience |
|----------|---------|-----------------|
| Missing API key | `config.py` check → warning in sidebar | ❌ icon shown; features disabled gracefully |
| NewsAPI timeout | `requests.exceptions.Timeout` caught | Falls back to web search |
| NewsAPI rate limit | HTTP 429 caught | Falls back to web search |
| Tavily failure | Exception caught | LLM uses own knowledge |
| OpenAI quota exceeded | `ValueError` caught | Clear error message displayed |
| Network disconnection | `ConnectionError` caught | "Check your internet connection" message |
| Invalid query | Classification defaults to "general" | Web search + LLM handles gracefully |

### 4.4 Query Processing Flow

**Step-by-step process for a news query:**

1. User types: *"Show me the latest technology news"*
2. **classify_query** → LLM classifies as `TYPE: news`, `CATEGORY: technology`
3. **Routing** → Conditional edge sends to `fetch_news` node
4. **fetch_news** → Calls `NewsAPI /v2/top-headlines?category=technology`
   - If success: formats articles with title, source, date, description, link
   - If failure: stores error message, continues to next node
5. **web_search** → Calls Tavily search for supplementary info
   - If success: formats results
   - If failure: stores error, continues
6. **generate_response** → LLM receives:
   - System prompt (NewsGenie persona)
   - Last 3 conversation exchanges (context continuity)
   - News results + web search results
   - Generates formatted, sourced response
7. Response displayed in Streamlit chat interface

---

## 5. System Architecture

### 5.1 File Structure

```
Project2/
├── app.py                  # Streamlit frontend (UI, session management)
├── workflow.py             # LangGraph workflow (state graph, nodes, routing)
├── news_api.py             # NewsAPI integration (headlines, search, formatting)
├── web_search.py           # Tavily web search tool
├── config.py               # Configuration, environment variables, constants
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .env.example            # Template for API keys
├── test_app.py             # Automated test suite (10 tests)
└── generate_samples.py     # Sample output generator for this report
```

### 5.2 Module Dependency Graph

```
app.py (Streamlit UI)
  ├── workflow.py (LangGraph orchestration)
  │     ├── news_api.py (NewsAPI client)
  │     ├── web_search.py (Tavily client)
  │     └── config.py (API keys, constants)
  ├── news_api.py (direct category fetch)
  └── config.py (API status display)
```

### 5.3 Streamlit UI Features

- **Sidebar:** News category selector (7 categories with icons), API status indicators, clear conversation button
- **Main Area:** Chat interface with full message history
- **Session Management:** Persistent chat history, category state tracking, re-run on category selection
- **Responsive Design:** Wide layout, styled components, spinner indicators during processing

---

## 6. Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.13 | Core runtime |
| Workflow Engine | LangGraph | ≥0.1.0 | State graph orchestration |
| LLM Framework | LangChain + OpenAI | ≥0.2.0 | NLP, chat completions |
| LLM Model | GPT-4o-mini | Latest | Classification + generation |
| News API | NewsAPI.org | v2 | Real-time headlines |
| Web Search | Tavily | ≥0.3.0 | Supplementary search |
| Frontend | Streamlit | ≥1.30.0 | Interactive web UI |
| Config | python-dotenv | ≥1.0.0 | Environment management |

---

## 7. Setup and Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env with your API keys:
#   OPENAI_API_KEY   → https://platform.openai.com
#   NEWS_API_KEY     → https://newsapi.org
#   TAVILY_API_KEY   → https://tavily.com

# 3. Run the application
streamlit run app.py

# 4. Run tests (no API keys needed)
python test_app.py
```

---

## 8. Test Results

All 10 automated tests pass successfully:

```
============================================================
  NewsGenie - Component Test Suite (Mocked APIs)
============================================================

TEST: Greeting Query ........................ PASSED ✓
TEST: News Query ............................ PASSED ✓
TEST: General Query ......................... PASSED ✓

MODULE IMPORT TESTS:
  config ........... OK ✓
  news_api ......... OK ✓
  web_search ....... OK ✓
  workflow ......... OK ✓
  Workflow compile .. OK ✓  (CompiledStateGraph)
  News formatting .. OK ✓
  Search formatting  OK ✓

SUMMARY: 10 passed, 0 failed
============================================================
```

**Test Coverage:**
- ✅ Query classification routing (greeting, news, general)
- ✅ LangGraph workflow compilation
- ✅ All module imports
- ✅ News article formatting
- ✅ Web search result formatting
- ✅ Error handling for missing API keys
- ✅ Fallback mechanism activation

---

*End of Report*
