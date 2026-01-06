import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(
        base_dir, "data", "processed", "imdb_2024_cleaned.csv"
    )
    return pd.read_csv(csv_path)

df = load_data()
