# utils.py
import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def load_excel_config(file_path):
    return pd.read_excel(file_path)

def save_time_entry(employee, project, job, date, hours):
    new_entry = {
        "Employee": employee,
        "Project": project,
        "Job": job,
        "Date": date.strftime("%Y-%m-%d"),
        "Hours": hours
    }

    if "time_entries" not in st.session_state:
        st.session_state["time_entries"] = []

    st.session_state["time_entries"].append(new_entry)

def get_all_entries():
    if "time_entries" in st.session_state:
        return pd.DataFrame(st.session_state["time_entries"])
    else:
        return pd.DataFrame(columns=["Employee", "Project", "Job", "Date", "Hours"])
