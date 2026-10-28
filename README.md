# StreamScope — Netflix Content Analytics

StreamScope is an end-to-end data analytics project built with **Python, Pandas, Matplotlib, and Streamlit**. It profiles and cleans a Netflix titles catalogue dataset, generates exploratory summaries and charts, and provides an interactive dashboard.

## Features

- Interactive KPIs for titles, movies, TV shows, and release years
- Filters by content type and release year
- Charts for content type, release-year trends, countries, genres, and ratings
- Search titles and download the filtered table as CSV
- Reproducible data-cleaning and EDA pipeline (`analysis.py`)
- Before/after data-quality reports and generated findings

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analysis.py
python -m streamlit run app.py
```

## Dataset

The repository contains a **small illustrative demo CSV** so the app can start without a separate download. For meaningful catalogue findings, download the Netflix Movies and TV Shows dataset from its original provider and save it as `data/netflix_titles.csv`. The app also lets you upload a CSV through the sidebar.

Dataset snapshots are third-party historical data, not a live Netflix catalogue. Verify the source and reuse terms of any dataset you download. Do not interpret catalogue counts as viewership or popularity.

## Deploy

Deploy `app.py` from this public GitHub repository using [Streamlit Community Cloud](https://share.streamlit.io/). Keep `requirements.txt` in the repository root. After adding `data/netflix_titles.csv`, redeploy/reboot the app if necessary.

## Project files

- `app.py` — interactive dashboard
- `analysis.py` — cleaning, profiling, feature engineering, EDA, charts, and reports
- `data/demo_netflix_titles.csv` — illustrative sample only
- `DATA_DICTIONARY.md` — column meanings
- `PROJECT_PLAN.md` — business questions and workflow
- `INTERVIEW_CONCEPTS.md` — concepts to explain in interviews
- `reports/FINAL_REPORT_TEMPLATE.md` — report template

## Resume bullet

**StreamScope — Netflix Content Analytics | Python, Pandas, Matplotlib, Streamlit** — Built a reproducible data-cleaning and exploratory-analysis pipeline with quality reports, engineered features, visualizations, and an interactive dashboard with filters, title search, and CSV export.
