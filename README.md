# StreamScope — Netflix Content Analytics

An interactive catalogue analytics dashboard built with Python, Pandas, Matplotlib, and Streamlit.

## Features
- KPI cards for title counts, movies, TV shows, and release years
- Filters by content type and release year
- Search titles and download filtered rows as CSV
- Charts for content types, release-year trends, countries, genres, and ratings
- Upload control for a full Netflix titles CSV
- Reproducible data-cleaning and exploratory-analysis pipeline with data-quality reports

## Run locally
Python 3.10+ is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analysis.py
python -m streamlit run app.py
```

## Dataset
The dashboard uses a local `data/netflix_titles.csv` when present. Otherwise, it attempts to load a historical 8,807-row Netflix titles snapshot from a public CSV mirror, then falls back to `data/demo_netflix_titles.csv` if the mirror is unavailable.

Original dataset listing: [Netflix Movies and TV Shows on Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows). The Kaggle listing identifies its dataset license as CC0: Public Domain. The app uses a historical mid-2021 catalogue snapshot, not Netflix's live/current catalogue. A public mirror is used as a convenience; availability is not guaranteed. The sidebar upload option lets you load another CSV at runtime.

For the separate analysis pipeline, save a permitted full CSV locally as `data/netflix_titles.csv`. That local data file is ignored by Git so it is not accidentally published without review.

## Deploy
This public repository is prepared for Streamlit Community Cloud:
1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app** and select this repository.
3. Set branch to `main` and main file path to `app.py`.
4. Click **Deploy**.

Dependencies are listed in `requirements.txt`. The hosted app first tries the public CSV mirror; if it cannot load, the app remains usable with the small demo and shows a warning.

## Project files
- `app.py` — interactive dashboard
- `analysis.py` — cleaning, profiling, feature engineering, EDA, charts, and reports
- `data/demo_netflix_titles.csv` — illustrative sample fallback
- `DATA_DICTIONARY.md` — column meanings
- `PROJECT_PLAN.md` — business questions and workflow
- `INTERVIEW_CONCEPTS.md` — interview preparation notes
- `reports/FINAL_REPORT_TEMPLATE.md` — report template

## Resume bullet
**StreamScope — Netflix Content Analytics | Python, Pandas, Matplotlib, Streamlit** — Built a reproducible data-cleaning and exploratory-analysis pipeline with quality reports, feature engineering, visualizations, and an interactive dashboard with filters, title search, and CSV export.

## Limitations
This is descriptive catalogue analysis. Catalogue counts do not prove popularity, watch time, or audience preference. Country and genre counts can overlap because a title may have multiple labels. Record the data provider, snapshot date, and license when reporting findings.
