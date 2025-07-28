import streamlit as st
from datetime import date
from utils import load_config, get_project_list, get_job_list, get_team_list, save_daily_log

# Load configuration files
project_df = load_config("Project_Config.xlsx")
job_df = load_config("Job_Config.xlsx")
team_df = load_config("Team_Config.xlsx")

st.set_page_config(page_title="Daily Work Entry", layout="centered")
st.title("📋 Daily Work Hour Entry")

with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("📅 Work Date", value=date.today())
        selected_person = st.selectbox("👤 Person", get_team_list(team_df))
    with col2:
        selected_project = st.selectbox("🏗️ Project", get_project_list(project_df))
        selected_job = st.selectbox("🔧 Job", get_job_list(job_df, selected_project))

    hours_worked = st.number_input("⏱️ Hours Worked", min_value=0.0, max_value=24.0, step=0.5)
    remarks = st.text_area("📝 Remarks (optional)", height=100)

    submitted = st.form_submit_button("✅ Submit Entry")

    if submitted:
        log_data = {
            "Date": selected_date,
            "Person": selected_person,
            "Project": selected_project,
            "Job": selected_job,
            "Hours": hours_worked,
            "Remarks": remarks
        }
        output_path = save_daily_log(log_data)
        st.success(f"Entry saved successfully to `{output_path}` ✅")
