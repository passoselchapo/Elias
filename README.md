
# Elias Assistant — Minimal Modular Backend (Version B)

A small, modular, and well-documented backend for the Elias assistant.
Designed to be simple, readable, and easy to extend over time. Comments in the code are in **Portuguese**.

---

## Project overview

This repository implements a minimal assistant backend with:

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
│ │ └── config.py
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
- httpx==0.24.1
- pydantic==1.10.11

Put those exact versions in `requirements.txt` for reproducibility.

---

## Environment variables

Create a `.env` file (or export the vars in your environment):

```

Database (Postgres)

DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/elias_db

FastAPI settings (optional)

HOST=127.0.0.1
PORT=8000
```

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
curl -X POST "http://127.0.0.1:8000/chat"   -H "Content-Type: application/json"   -d '{"message": "Hello Elias, make a plan for a trip to São Paulo"}'

```

# What each module does

## `app/core/config.py`
Central configuration loader  
Reads `.env` and exposes all relevant settings used by the system.

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

1. Process user message  
2. Persist conversation

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
Write unit tests.

### Logging
Use Python’s logging:
- Default: `INFO`
- Switch to `DEBUG` only during development.

### Extensibility
For new features, integrate them cleanly with the orchestrator.

### Security
Do **not** commit `.env` or API keys.  
Use environment variables or secret managers.

---

# Notes about comments & documentation

- All in-code comments are written in **Português**  
  Helpful for onboarding collaborators who prefer local-language annotations.
- This README is written in **English** to align with tooling, CI, and collaboration norms.

---

# Next recommended steps

- Add tests for orchestrator behavior.
- Add GitHub Actions CI for linting + tests.
- Create a simple web UI or Postman collection for manual QA.

---

If you want, I can now create:

- `app/core/*` (config)
- `app/db/*` (database + models)
- `app/api.py` and `app/cli.py`
- Or even package the full project into a **zip-ready block of files**

Just tell me which files you want next.
