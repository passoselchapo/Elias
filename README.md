
# Elias Assistant — Minimal Modular Backend (Version B)

A small, modular, and well-documented backend for the Elias assistant.  
Designed to be simple, readable, and easy to extend over time. Comments in the code are in **Portuguese**.

---

## Project overview

This repository implements a minimal assistant backend with:

- Persona selection (multiple personas supported)
- Importance scoring (heuristic)
- Summarization (LLM-backed with a local fallback)
- Conversation persistence (Postgres via SQLAlchemy)
- A small orchestrator that coordinates the flow
- FastAPI endpoint (`/chat`) and an optional CLI entrypoint

The design goal is **clear separation of concerns** so that new features can be added incrementally and safely.


## Repository layout

```

elias_assistant/
│
├── app/
│ ├── core/
│ │ ├── config.py
│ │ ├── personas.py
│ │ ├── scorer.py
│ │ └── summarizer.py
│ │
│ ├── services/
│ │ └── orchestrator.py # (this file)
│ │
│ ├── db/
│ │ ├── database.py
│ │ └── models.py
│ │
│ ├── api.py
│ └── cli.py
│
├── requirements.txt
└── README.md

```

## Requirements

Developed and tested with (recommended versions):

- Python 3.10+
- fastapi==0.95.2
- uvicorn==0.22.0
- sqlalchemy==2.0.20
- psycopg2-binary==2.9.7
- python-dotenv==1.0.0
- openai==1.0.0
- httpx==0.24.1
- pydantic==1.10.11

Put those exact versions in `requirements.txt` for reproducibility.

---

## Environment variables

Create a `.env` file (or export the vars in your environment):

```

Database (Postgres)

DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/elias_db

OpenAI (optional, used for summarization and responses)

OPENAI_API_KEY=sk-xxxx
OPENAI_API_BASE=https://api.openai.com/v1

OPENAI_MODEL=gpt-4o-mini

FastAPI settings (optional)

HOST=127.0.0.1
PORT=8000
```


If `OPENAI_API_KEY` is not provided the system falls back to simulated/local behaviour so you can still develop.

---

## Quickstart

1. Create Python venv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt ```
```

1. Initialize database (example using a local Postgres instance):

2. Open a Python REPL in the project root and run:

```python
from app.db.database import engine
from app.db.models import Base
Base.metadata.create_all(bind=engine)
```

3. Run the API:

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload

```
4. Example POST /chat:

```bash
curl -X POST "http://127.0.0.1:8000/chat"   -H "Content-Type: application/json"   -d '{"message": "Hello Elias, make a plan for a trip to São Paulo", "persona": "travel"}'

```

# What each module does

## `app/core/config.py`
Central configuration loader  
Reads `.env` and exposes all relevant settings used by the system.

---

## `app/core/personas.py`
Defines all personas and their system instructions.  
Add new personas by inserting new dictionary entries into `PERSONAS`.

---

## `app/core/scorer.py`
Implements the importance scoring logic (heuristic).  
This module can later be replaced or extended with ML/LLM-based scoring.

---

## `app/core/summarizer.py`
Summarization wrapper.  
Uses OpenAI when available, with an automatic local fallback for offline development.

---

## `app/db/database.py` & `app/db/models.py`
Database layer:
- SQLAlchemy engine and session (`database.py`)
- Conversation model (`models.py`)

Responsible for persistence of all interactions.

---

## `app/services/orchestrator.py`
**Main orchestrator** — central pipeline of the system.  
Coordinates the entire process:

1. Score importance  
2. Summarize message  
3. Generate persona response  
4. Persist conversation

This is one of the core modules of the project.

---

## `app/api.py`
FastAPI endpoint layer.  
Thin by design — delegates all heavy logic to the orchestrator.

---

## `app/cli.py`
Optional command-line interface (REPL) for local testing and debugging.

---

# Development notes & guidelines

### Small increments
Add one small feature at a time and keep changes focused.

### Tests
Write unit tests early for:
- scorer
- summarizer
- personas

They are small and isolated, perfect for early coverage.

### Logging
Use Python’s logging:
- Default: `INFO`
- Switch to `DEBUG` only during development.

### Personas
Keep persona prompts short and focused.  
Persona metadata (tone, max_tokens, etc.) lives inside `personas.py`.

### Extensibility
For long-term memory or retrieval features:
- Create `services/memory.py`
- Expose `store()` and `retrieve()` interfaces
- Plug into orchestrator cleanly

### Security
Do **not** commit `.env` or API keys.  
Use environment variables or secret managers.

---

# How to add a new persona

1. Edit `app/core/personas.py`  
2. Add a new entry to the `PERSONAS` dict  
3. (Optional) Add persona-specific config such as `max_tokens`  
4. Done — orchestrator automatically uses it via `get_persona()`

No other code updates needed.

---

# How to change to an LLM-based importance scorer

1. Implement a new scorer inside:
   - `app/core/scorer.py`, or  
   - create `scorer_llm.py`
2. Replace the call to `scorer.heuristic_importance()` inside:
   - `app/services/orchestrator.py`
3. Add a small test ensuring scores stay within the 0..1 range.

---

# Notes about comments & documentation

- All in-code comments are written in **Português**  
  Helpful for onboarding collaborators who prefer local-language annotations.
- This README is written in **English** to align with tooling, CI, and collaboration norms.

---

# Next recommended steps

- Add tests for orchestrator behavior (OpenAI fallback included)
- Add GitHub Actions CI for linting + tests
- Create a simple web UI or Postman collection for manual QA

---

If you want, I can now create:

- `app/core/*` (config, personas, scorer, summarizer)  
- `app/db/*` (database + models)  
- `app/api.py` and `app/cli.py`  
- Or even package the full project into a **zip-ready block of files**

Just tell me which files you want next.
