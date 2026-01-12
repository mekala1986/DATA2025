# app.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="IMDb 2024 Movies Dashboard",
    layout="wide"
)

st.title("🎬 IMDb 2024 Movies Analysis Dashboard")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    # Replace with your CSV path
    df = pd.read_csv("movies_2024.csv")
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🎯 Filter Movies")
genres = df['genre'].dropna().unique().tolist()
selected_genres = st.sidebar.multiselect("Select Genre(s)", genres)

rating_range = st.sidebar.slider("IMDb Rating Range", 1.0, 10.0, (1.0, 10.0))

# -----------------------------
# Filter Dataset
# -----------------------------
filtered_df = df.copy()

# Filter by genre
if selected_genres:
    filtered_df = filtered_df[filtered_df['genre'].apply(lambda x: any(g in x for g in selected_genres))]

# Filter by rating
filtered_df = filtered_df[(filtered_df['rating'] >= rating_range[0]) & (filtered_df['rating'] <= rating_range[1])]

# -----------------------------
# Metrics
# -----------------------------
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Movies", filtered_df.shape[0])
col2.metric("Average Rating", round(filtered_df['rating'].mean(), 2))
col3.metric("Total Votes", int(filtered_df['votes'].sum()))

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📄 Movie Dataset Preview")
st.dataframe(filtered_df)

# -----------------------------
# Visual Analysis
# -----------------------------
st.subheader("📈 Movies by Rating (Ascending)")

# Sort by rating ascending
sorted_df = filtered_df.sort_values(by='rating', ascending=True)

plt.figure(figsize=(12,8))
plt.barh(sorted_df['movie_name'], sorted_df['rating'], color='skyblue')
plt.xlabel("Rating")
plt.ylabel("Movie Name")
plt.title("Movies by Rating (Ascending)")
plt.tight_layout()
st.pyplot(plt)

# -----------------------------
# Rating Distribution Histogram
# -----------------------------
st.subheader("📊 Rating Distribution")

plt.figure(figsize=(10,5))
plt.hist(filtered_df['rating'], bins=20, color='orange', edgecolor='black')
plt.xlabel("Rating")
plt.ylabel("Number of Movies")
plt.title("IMDb Rating Distribution")
plt.tight_layout()
st.pyplot(plt)
