import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_team_config, load_project_config, load_job_config, get_team_members, append_to_time_report

st.set_page_config(page_title="Nhập dữ liệu thời gian làm việc", layout="wide")
st.title("📝 Nhập dữ liệu thời gian làm việc")

# Load configs
team_df = load_team_config("Team_Config.xlsx")
project_df = load_project_config("Project_Config.xlsx")
job_df = load_job_config("Job_Config.xlsx")

selected_date = st.date_input("🗓️ Ngày làm việc", value=datetime.today())
team_leaders = team_df['Group Leader'].dropna().unique().tolist()
selected_leader = st.selectbox("👤 Chọn nhóm trưởng", team_leaders)

if selected_leader:
    members = get_team_members(team_df, selected_leader)
    with st.form("data_entry_form", clear_on_submit=True):
        rows = []
        for member in members:
            st.subheader(f"🧑‍💼 {member}")
            project = st.selectbox("• Dự án", project_df['Project'], key=f"proj_{member}")
            job = st.selectbox("• Công việc", job_df['Job'], key=f"job_{member}")
            hours = st.number_input("• Giờ làm", 0.0, 24.0, 8.0, 0.5, key=f"hours_{member}")
            rows.append({
                "Ngày làm": selected_date,
                "Nhóm trưởng": selected_leader,
                "Tên nhân sự": member,
                "Dự án": project,
                "Công việc": job,
                "Số giờ": hours
            })
        submitted = st.form_submit_button("📥 Ghi dữ liệu")
        if submitted:
            df = pd.DataFrame(rows)
            append_to_time_report(df)
            st.success("✅ Dữ liệu đã được ghi vào báo cáo!")
