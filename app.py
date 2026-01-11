import os
import pandas as pd
import streamlit as st
# Matplotlib safe backend for Streamlit Cloud
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="IMDb 2024 Movies Dashboard",
    layout="wide"
)

st.title("🎬 IMDb 2024 Movies Analysis Dashboard")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "imdb_2024_cleaned.csv")
    return pd.read_csv(csv_path)

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("🎛 Filter Movies")

# Year filter (if column exists)
if "year" in df.columns:
    year_options = sorted(df["year"].dropna().unique())
    selected_years = st.sidebar.multiselect(
        "Select Year(s)", year_options, default=year_options
    )
    df = df[df["year"].isin(selected_years)]

# Genre filter (if column exists)
if "genre" in df.columns:
    genre_options = sorted(df["genre"].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Select Genre(s)", genre_options, default=genre_options
    )
    df = df[df["genre"].isin(selected_genres)]

# Rating filter (if column exists)
if "rating" in df.columns:
    min_rating = float(df["rating"].min())
    max_rating = float(df["rating"].max())
    rating_range = st.sidebar.slider(
        "IMDb Rating Range",
        min_rating,
        max_rating,
        (min_rating, max_rating)
    )
    df = df[(df["rating"] >= rating_range[0]) & (df["rating"] <= rating_range[1])]

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🎥 Total Movies", len(df))
if "rating" in df.columns:
    col2.metric("⭐ Average Rating", round(df["rating"].mean(), 2))
if "votes" in df.columns:
    col3.metric("🗳 Total Votes", int(df["votes"].sum()))

# -----------------------------
# Data preview
# -----------------------------
st.subheader("📄 Movie Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

# -----------------------------
# Charts
# -----------------------------
st.subheader("📊 Visual Analysis")

col4, col5 = st.columns(2)

# Rating distribution
if "rating" in df.columns:
    with col4:
        st.markdown("**Rating Distribution**")
        fig, ax = plt.subplots()
        ax.hist(df["rating"].dropna(), bins=10)
        ax.set_xlabel("IMDb Rating")
        ax.set_ylabel("Number of Movies")
        st.pyplot(fig)
st.subheader("Movie Dataset Preview")

# 🔹 Sort option
sort_order = st.selectbox(
    "Order by Rating",
    ["Highest to Lowest", "Lowest to Highest"]
)

# 🔹 Apply sorting AFTER filtering
if sort_order == "Highest to Lowest":
    filtered_df = filtered_df.sort_values(by="rating", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="rating", ascending=True)

# 🔹 Reset index (THIS IS VERY IMPORTANT)
filtered_df = filtered_df.reset_index(drop=True)

# 🔹 Display
st.dataframe(filtered_df)

# Genre count
if "genre" in df.columns:
    with col5:
        st.markdown("**Top Genres**")
        genre_counts = df["genre"].value_counts().head(10)
        fig, ax = plt.subplots()
        genre_counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Genre")
        ax.set_ylabel("Number of Movies")
        st.pyplot(fig)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("📌 IMDb 2024 Data Analysis | Built with Streamlit")




