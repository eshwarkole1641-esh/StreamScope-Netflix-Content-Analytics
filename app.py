from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="StreamScope", page_icon="🎬", layout="wide")
st.title("🎬 StreamScope — Netflix Content Analytics")
st.caption("Explore catalogue composition, release trends, genres, countries, and ratings.")

ROOT = Path(__file__).parent
DEFAULT_DATA = ROOT / "data" / "netflix_titles.csv"
DEMO_DATA = ROOT / "data" / "demo_netflix_titles.csv"
uploaded = st.sidebar.file_uploader("Upload the full Netflix titles CSV", type=["csv"])

@st.cache_data(show_spinner=False)
def read_csv(file_or_path):
    return pd.read_csv(file_or_path)

try:
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        source = "Uploaded dataset"
    elif DEFAULT_DATA.exists():
        df = read_csv(DEFAULT_DATA)
        source = "Full dataset file"
    else:
        df = read_csv(DEMO_DATA)
        source = "DEMO DATA — illustrative rows only"
        st.sidebar.warning("Showing only a tiny demo dataset. Upload the full Netflix CSV for meaningful analysis.")
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

# Normalize the expected fields and provide clear feedback if the upload is incompatible.
df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
if not {"type", "title"}.issubset(df.columns):
    st.error("CSV must include at least the 'type' and 'title' columns.")
    st.stop()
for col in ["release_year", "country", "rating", "listed_in", "date_added", "duration"]:
    if col not in df:
        df[col] = pd.NA

df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
for col in ["type", "country", "rating", "listed_in", "title"]:
    df[col] = df[col].astype("string").str.strip()
for col in ["country", "rating", "listed_in"]:
    df[col] = df[col].fillna("Unknown").replace("", "Unknown")

st.caption(f"Data source: {source} · {len(df):,} rows")
types = sorted(df["type"].dropna().astype(str).unique().tolist())
selected_types = st.sidebar.multiselect("Content type", types, default=types)
years = df["release_year"].dropna()
if not years.empty and years.min() < years.max():
    year_range = st.sidebar.slider("Release year", int(years.min()), int(years.max()), (int(years.min()), int(years.max())))
else:
    year_range = (int(years.min()), int(years.max())) if not years.empty else (0, 9999)

view = df[df["type"].isin(selected_types)].copy()
view = view[view["release_year"].between(*year_range) | view["release_year"].isna()]
search = st.text_input("Search titles", placeholder="Type a title name...")
if search:
    view = view[view["title"].astype(str).str.contains(search, case=False, na=False)]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Titles", f"{len(view):,}")
k2.metric("Movies", f"{(view['type'] == 'Movie').sum():,}")
k3.metric("TV Shows", f"{(view['type'] == 'TV Show').sum():,}")
k4.metric("Release years", f"{view['release_year'].nunique():,}")

left, right = st.columns(2)
with left:
    st.subheader("Movies vs TV Shows")
    counts = view["type"].value_counts()
    if not counts.empty:
        fig, ax = plt.subplots(figsize=(7, 4))
        counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Content type"); ax.set_ylabel("Titles")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    else:
        st.info("No records match the current filters.")
with right:
    st.subheader("Titles by release year")
    by_year = view.dropna(subset=["release_year"]).groupby("release_year").size().sort_index()
    if not by_year.empty:
        fig, ax = plt.subplots(figsize=(7, 4))
        by_year.plot(ax=ax)
        ax.set_xlabel("Release year"); ax.set_ylabel("Titles")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    else:
        st.info("No release-year data for the current filters.")

left, right = st.columns(2)
with left:
    st.subheader("Top countries")
    country_counts = view[view["country"] != "Unknown"]["country"].dropna().str.split(", ").explode().value_counts().head(10)
    if not country_counts.empty:
        fig, ax = plt.subplots(figsize=(7, 4))
        country_counts.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Titles"); ax.set_ylabel("Country")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    else:
        st.info("Country information is unavailable for these records.")
with right:
    st.subheader("Top genres")
    genre_counts = view[view["listed_in"] != "Unknown"]["listed_in"].dropna().str.split(", ").explode().value_counts().head(10)
    if not genre_counts.empty:
        fig, ax = plt.subplots(figsize=(7, 4))
        genre_counts.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Titles"); ax.set_ylabel("Genre")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    else:
        st.info("Genre information is unavailable for these records.")

st.subheader("Ratings")
rating_counts = view[view["rating"] != "Unknown"]["rating"].value_counts().head(12)
if not rating_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    rating_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Rating"); ax.set_ylabel("Titles"); ax.tick_params(axis="x", rotation=45)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)
else:
    st.info("Rating information is unavailable for these records.")

columns = [c for c in ["title", "type", "release_year", "country", "rating", "duration", "listed_in", "date_added"] if c in view]
st.subheader("Catalogue records")
st.dataframe(view[columns], width="stretch", hide_index=True)
st.download_button("Download filtered CSV", data=view.to_csv(index=False).encode("utf-8"), file_name="streamscope_filtered.csv", mime="text/csv")
st.info("This is descriptive catalogue analysis. Catalogue counts do not prove popularity, viewership, or audience preference. Genre and country totals can overlap because a title may have multiple labels.")
