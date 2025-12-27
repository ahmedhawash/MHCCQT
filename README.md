# Quality Tracker – Streamlit App

A lightweight, file-based **Quality Monitoring and Evaluation** application built with **Streamlit**.  
It allows reviewers to evaluate agents using configurable question sets, store results safely, and analyze performance over time.

## Key Features
- Dynamic evaluation forms driven by CSV question sets
- Per-question scoring, total and normalized percentage scores
- Reviewer comments and submission locking to avoid duplicates
- Results saved as CSV (no database required)
- Simple analytics: recent evaluations, averages, and charts

## Quickstart
Prerequisites: Python 3.9+ and `pip`.

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_app.py
```

Open the URL printed by Streamlit (usually http://localhost:8501).

## Project Layout
- `streamlit_app.py` — main entry point
- `pages/` — Streamlit multipage modules:
  - `quality_tracker.py` — evaluation form
  - `get_started.py` — results and analytics
  - `configuration.py` — optional settings
- `data/`
  - `coaches/coaches.csv` — coach list
  - `agents/agents.csv` — agent list
  - `questions/` — versioned question CSVs (timestamped filenames)
  - `results/` — generated result CSVs

## CSV formats (overview)
- Coaches (`data/coaches/coaches.csv`):

```csv
id,name
1,John Doe
```

- Agents (`data/agents/agents.csv`):

```csv
id,name
101,Jane Smith
```

- Questions (`data/questions/questions_YYYYMMDDHHMMSS.csv`):

```csv
number,question,weight
1,Did the agent greet the customer?,20
2,Was the issue resolved?,30
3,Was proper closing used?,50
```

Rules:
- Exactly three columns: `number`, `question`, `weight`.
- `number` should be sequential starting at 1.
- `weight` values should sum to 100.

- Results filenames: `{questions_timestamp}_results_{submission_date}.csv` (each row = one evaluation; contains coach/agent info, dates, per-question answers, scores, total and normalized score, and reviewer comments).

## Pages / UX
- Evaluation (`quality_tracker`): choose coach and agent, pick dates, answer the question set, submit. The form locks after successful submission and prevents duplicates.
- Results & Analytics (`get_started`): browse recent results, view averages and charts.
- Configuration (`configuration`): small helper page for optional settings and CSV uploads (if present).

## Design Notes
- No database: CSV files keep the app simple, portable, and auditable.
- Versioned question sets: changing questions creates a new CSV, preserving past evaluations.
