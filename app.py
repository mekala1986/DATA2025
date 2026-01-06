import os
import pandas as pd
import streamlit as st

# 🔍 DEBUG – paste here
st.write("Root files:", os.listdir("."))

if os.path.exists("data"):
    st.write("Data folder:", os.listdir("data"))
else:
    st.write("Data folder: NO data folder")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "action.csv")  # example
    return pd.read_csv(csv_path)

df = load_data()
