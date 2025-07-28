import streamlit as st
from datetime import date
from utils import (
    load_config,
    get_team_list,
    get_team_members,
    get_project_list,
    get_job_list,
    get_employee_id,
    get_project_code,
    get_job_info,
    save_to_time_report
)

# Load config files
project_df = load_config("Project_Config.xlsx")
job_df = load_config("Job_Config.xlsx")
team_df = load_config("Team_Config.xlsx")

# Page layout
st.set_page_config(page_title="Daily Work Entry", layout="wide")
st.title("📋 Daily Work Hour Entry")

# Select working date and team leader
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("📅 Ngày làm việc", value=date.today())
with col2:
    selected_leader = st.selectbox("👤 Nhóm trưởng", get_team_list(team_df))

# Show form if team leader is selected
if selected_leader:
    members = get_team_members(team_df, selected_leader)
    st.markdown(f"### 👥 Thành viên trong nhóm **{selected_leader}**")
    submitted = False

    with st.form("entry_form", clear_on_submit=True):
        member_entries = []

        for member in members:
            st.markdown(f"#### 👤 {member}")
            col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
            with col1:
                present = st.checkbox("Có mặt", key=f"{member}_present")
            with col2:
                hours = st.number_input("Giờ làm", 0.0, 24.0, 8.0, 0.5, key=f"{member}_hours")
            with col3:
                selected_project = st.selectbox(
                    "Dự án", get_project_list(project_df), key=f"{member}_project"
                )
            with col4:
                selected_job = st.selectbox(
                    "Công việc", get_job_list(job_df, selected_project), key=f"{member}_job"
                )

            if present:
                emp_id = get_employee_id(team_df, member)
                proj_code = get_project_code(project_df, selected_project)
                job_code, workcenter, task = get_job_info(job_df, selected_job)

                member_entries.append({
                    "Date": selected_date,
                    "Project Name": selected_project,
                    "Project Code": proj_code,
                    "Job Name": selected_job,
                    "Job Code": job_code,
                    "Employee": member,
                    "Employee ID": emp_id,
                    "Team": selected_leader,
                    "Workcenter": workcenter,
                    "Task": task,
                    "Hours": hours,
                })

        submitted = st.form_submit_button("✅ Gửi dữ liệu")

    if submitted:
        if member_entries:
            save_to_time_report(member_entries)
            st.success("✅ Dữ liệu đã được lưu thành công vào Time_report.xlsm!")
        else:
            st.warning("⚠️ Không có thành viên nào được chọn là 'Có mặt'.")
