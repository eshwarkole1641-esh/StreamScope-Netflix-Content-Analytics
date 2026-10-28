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
The repository includes `data/demo_netflix_titles.csv`, a tiny **illustrative demo only**. The full Netflix CSV is not included because its source and redistribution license must be checked before publicly republishing it.

For meaningful analysis, download a dataset from a source whose terms allow your intended use, then upload it using the dashboard sidebar. To run the separate analysis pipeline, save it locally as `data/netflix_titles.csv`. The local full-data file is intentionally ignored by Git.

## Deploy
This repository is public and prepared for Streamlit Community Cloud:
1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app** and select this repository.
3. Set branch to `main` and main file path to `app.py`.
4. Click **Deploy**.

The app starts with the demo CSV until a full dataset is uploaded in the sidebar or made available in the runtime. Dependencies are listed in `requirements.txt`.

## Project files
- `app.py` — interactive dashboard
- `analysis.py` — cleaning, profiling, feature engineering, EDA, charts, and reports
- `data/demo_netflix_titles.csv` — illustrative sample
- `DATA_DICTIONARY.md` — column meanings
- `PROJECT_PLAN.md` — business questions and workflow
- `INTERVIEW_CONCEPTS.md` — interview preparation notes
- `reports/FINAL_REPORT_TEMPLATE.md` — report template

## Resume bullet
**StreamScope — Netflix Content Analytics | Python, Pandas, Matplotlib, Streamlit** — Built a reproducible data-cleaning and exploratory-analysis pipeline with quality reports, feature engineering, visualizations, and an interactive dashboard with filters, title search, and CSV export.

## Limitations
This is descriptive catalogue analysis. Catalogue counts do not prove popularity, watch time, or audience preference. Country and genre counts can overlap because a title may have multiple labels. Record the data provider, download date, and license when reporting findings.
