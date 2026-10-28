from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "netflix_titles.csv"
DEMO = ROOT / "data" / "demo_netflix_titles.csv"
OUT = ROOT / "outputs"
REPORTS = ROOT / "reports"
OUT.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

# 1. Load the full dataset when available; otherwise use the clearly labeled demo.
path = DATA if DATA.exists() else DEMO
raw = pd.read_csv(path)
print("Source:", path.name, "| Raw shape:", raw.shape)

# 2. Profile the raw data.
pd.DataFrame({
    "column": raw.columns,
    "dtype": [str(x) for x in raw.dtypes],
    "missing_count": raw.isna().sum().values,
    "missing_percent": (raw.isna().mean().values * 100).round(2),
    "unique_values": [raw[c].nunique(dropna=True) for c in raw.columns],
}).to_csv(OUT / "data_quality_before.csv", index=False)

# 3. Normalize column names and trim text.
df = raw.copy()
df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].astype("string").str.strip()
    df[col] = df[col].replace({"": pd.NA, "NA": pd.NA, "N/A": pd.NA, "null": pd.NA})

# 4. Remove exact duplicates and validate required fields.
before_rows = len(df)
df = df.drop_duplicates()
duplicates_removed = before_rows - len(df)
for col in ["title", "type"]:
    if col not in df.columns:
        raise ValueError(f"Required column missing: {col}")

if "release_year" in df:
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")
if "date_added" in df:
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
if "type" in df:
    df["type"] = df["type"].str.title().replace({"Tv Show": "TV Show"})

pd.DataFrame({
    "column": df.columns,
    "missing_count": df.isna().sum().values,
    "missing_percent": (df.isna().mean().values * 100).round(2),
}).to_csv(OUT / "missing_values_report.csv", index=False)

# Preserve missingness in dates and numeric fields; label descriptive gaps explicitly.
for col in ["director", "cast", "country", "rating", "duration", "listed_in", "description"]:
    if col in df:
        df[col] = df[col].fillna("Unknown")

# 5. Feature engineering.
if "date_added" in df:
    df["date_added_year"] = df["date_added"].dt.year.astype("Int64")
    df["date_added_month"] = df["date_added"].dt.month.astype("Int64")
if "duration" in df:
    df["duration_value"] = pd.to_numeric(
        df["duration"].astype("string").str.extract(r"(\d+)")[0], errors="coerce"
    ).astype("Int64")
    df["duration_unit"] = df["duration"].astype("string").str.extract(r"([A-Za-z]+)$")[0].fillna("Unknown")
if "listed_in" in df:
    df["primary_genre"] = df["listed_in"].apply(
        lambda x: str(x).split(",")[0].strip() if pd.notna(x) and str(x) != "Unknown" else "Unknown"
    )
if "country" in df:
    df["primary_country"] = df["country"].apply(
        lambda x: str(x).split(",")[0].strip() if pd.notna(x) and str(x) != "Unknown" else "Unknown"
    )

# 6. Post-cleaning quality checks and cleaned export.
pd.DataFrame({
    "column": df.columns,
    "dtype": [str(x) for x in df.dtypes],
    "missing_count": df.isna().sum().values,
    "missing_percent": (df.isna().mean().values * 100).round(2),
    "unique_values": [df[c].nunique(dropna=True) for c in df.columns],
}).to_csv(OUT / "data_quality_after.csv", index=False)
df.to_csv(OUT / "cleaned_netflix_titles.csv", index=False)

# 7. Summary metrics and EDA tables.
metrics = {
    "source_file": path.name,
    "raw_rows": int(len(raw)),
    "clean_rows": int(len(df)),
    "duplicate_rows_removed": int(duplicates_removed),
    "raw_missing_cells": int(raw.isna().sum().sum()),
    "movies": int((df["type"] == "Movie").sum()),
    "tv_shows": int((df["type"] == "TV Show").sum()),
}
(OUT / "summary_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
df["type"].value_counts().rename_axis("type").reset_index(name="count").to_csv(OUT / "content_type_counts.csv", index=False)
if "release_year" in df:
    df.dropna(subset=["release_year"]).groupby("release_year").size().rename("count").reset_index().to_csv(OUT / "titles_by_release_year.csv", index=False)
if "rating" in df:
    df["rating"].value_counts().rename_axis("rating").reset_index(name="count").to_csv(OUT / "rating_counts.csv", index=False)
if "listed_in" in df:
    df[df["listed_in"] != "Unknown"]["listed_in"].str.split(", ").explode().value_counts().rename_axis("genre").reset_index(name="count").to_csv(OUT / "genre_counts.csv", index=False)
if "country" in df:
    df[df["country"] != "Unknown"]["country"].str.split(", ").explode().value_counts().rename_axis("country").reset_index(name="count").to_csv(OUT / "country_counts.csv", index=False)

# 8. Create charts.
def save_bar(series, title, xlabel, ylabel, filename, horizontal=False):
    if series.empty:
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    values = series.sort_values() if horizontal else series
    values.plot(kind="barh" if horizontal else "bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if not horizontal:
        ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=160)
    plt.close(fig)

save_bar(df["type"].value_counts(), "Titles by Type", "Type", "Titles", "titles_by_type.png")
if "release_year" in df:
    yearly = df["release_year"].dropna().value_counts().sort_index()
    if not yearly.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        yearly.plot(ax=ax)
        ax.set_title("Titles by Release Year")
        ax.set_xlabel("Release year")
        ax.set_ylabel("Titles")
        fig.tight_layout()
        fig.savefig(OUT / "titles_by_release_year.png", dpi=160)
        plt.close(fig)
if "listed_in" in df:
    save_bar(df[df["listed_in"] != "Unknown"]["listed_in"].str.split(", ").explode().value_counts().head(10),
             "Top 10 Genres", "Titles", "Genre", "top_genres.png", True)
if "country" in df:
    save_bar(df[df["country"] != "Unknown"]["country"].str.split(", ").explode().value_counts().head(10),
             "Top 10 Countries", "Titles", "Country", "top_countries.png", True)
if "rating" in df:
    save_bar(df[df["rating"] != "Unknown"]["rating"].value_counts().head(12),
             "Content Ratings", "Rating", "Titles", "rating_distribution.png")

# 9. Findings and a clear warning for demo data.
findings = [
    f"Source file: {path.name}",
    f"Rows before cleaning: {len(raw)}; rows after exact-duplicate removal: {len(df)}.",
    f"Exact duplicate rows removed: {duplicates_removed}.",
    f"Missing cells in raw data: {int(raw.isna().sum().sum())}.",
]
if path.name == DEMO.name:
    findings.append("WARNING: demo data only; do not report these numbers as real Netflix catalogue findings.")
else:
    findings.append("Descriptive findings only: catalogue counts do not prove popularity or viewer preference.")
(REPORTS / "findings.txt").write_text("\n".join("- " + item for item in findings), encoding="utf-8")
print("Complete. Review outputs/ and reports/findings.txt")
