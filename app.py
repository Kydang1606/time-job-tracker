# app.py
import streamlit as st
import pandas as pd
from utils import (
    load_excel_config,
    filter_data_by_config,
    show_comparison_chart
)

st.set_page_config(page_title="Compare Projects Over Time", layout="wide")

st.title("📊 Project Time Comparison")

# --- Load Configs ---
with st.sidebar:
    st.header("🛠️ Configuration")
    project_df = load_excel_config("Project_Config.xlsx")
    team_df = load_excel_config("Team_Config.xlsx")
    job_df = load_excel_config("Job_Config.xlsx")

    mode = st.radio("Select Comparison Mode", ["Compare Projects in a Month", "Compare Projects Over Time"])

# --- Upload Raw Data ---
uploaded_file = st.file_uploader("Upload Raw Data File (.xlsx)", type="xlsx")
if uploaded_file:
    raw_df = pd.read_excel(uploaded_file, sheet_name=0)

    # --- Filter Config ---
    config = filter_data_by_config(mode, project_df, team_df, job_df)

    if config:
        st.success("✅ Configuration loaded. Showing chart:")
        show_comparison_chart(raw_df, config, mode)
    else:
        st.warning("⚠️ Please complete all config selections.")
