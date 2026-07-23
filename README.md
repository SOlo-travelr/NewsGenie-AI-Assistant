# NewsGenie: AI News and Information Assistant

NewsGenie is a Streamlit-based AI assistant that combines real-time news retrieval and web search with an LLM-powered response workflow. It can answer general questions, fetch category-based headlines, and provide concise, source-aware responses.

## Suggested Repository Details

- **Repository name:** `newsgenie-ai-assistant`
- **Description:** `AI-powered Streamlit assistant that uses LangGraph, OpenAI, NewsAPI, and Tavily to deliver real-time news and general answers.`

## Features

- Conversational UI built with Streamlit chat components
- LLM-based query classification (`news`, `general`, `greeting`)
- Real-time news headlines and topic search via NewsAPI
- Supplementary web search via Tavily
- LangGraph state machine for deterministic routing and response generation
- Graceful fallback behavior when external APIs fail

## Project Structure

- `app.py`: Streamlit app entry point and UI
- `workflow.py`: LangGraph workflow and routing logic
- `news_api.py`: NewsAPI integration helpers
- `web_search.py`: Tavily search integration helpers
- `config.py`: Environment variable and app configuration
- `test_app.py`: Test cases
- `requirements.txt`: Python dependencies
- `SUBMISSION_REPORT.md`: Detailed design and architecture report

## Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain + OpenAI
- NewsAPI
- Tavily Search API

## Quick Start

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd newsgenie-ai-assistant
```

### 2. Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

You can copy from `.env.example` and fill in real values.

### 5. Run the app

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## How It Works

1. User enters a query in the chat UI.
2. `classify_query` labels intent and optional news category.
3. News queries call NewsAPI, then optionally web search.
4. General queries call web search directly.
5. `generate_response` synthesizes gathered context with recent chat history.

## Testing

Run tests with:

```bash
pytest -q
```

## Notes

- Keep API keys private and never commit your real `.env`.
- The app is designed to continue responding even when one data source is unavailable.

## License

Add a license file if you plan to distribute this repository publicly.
