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

st.set_page_config(page_title="Daily Work Entry", layout="wide")
st.title("📋 Daily Work Hour Entry")

# Upload file Time_report.xlsm (bắt buộc để ghi dữ liệu)
uploaded_file = st.file_uploader("📂 Upload file Time_report.xlsm", type=["xlsm"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("📅 Ngày làm việc", value=date.today())
    with col2:
        selected_leader = st.selectbox("👤 Nhóm trưởng", get_team_list(team_df))

    if selected_leader:
        members = get_team_members(team_df, selected_leader)
        st.markdown(f"### 👥 Thành viên trong nhóm **{selected_leader}**")

        with st.form("entry_form", clear_on_submit=True):
            member_entries = []

            for member in members:
                st.markdown(f"#### 👤 {member}")
                c1, c2, c3, c4 = st.columns([1, 1, 2, 2])
                with c1:
                    present = st.checkbox("Có mặt", key=f"{member}_present")
                with c2:
                    hours = st.number_input("Giờ làm", 0.0, 24.0, 8.0, 0.5, key=f"{member}_hours")
                with c3:
                    selected_project = st.selectbox("Dự án", get_project_list(project_df), key=f"{member}_project")
                with c4:
                    selected_job = st.selectbox("Công việc", get_job_list(job_df, selected_project), key=f"{member}_job")

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
                try:
                    updated_file = save_to_time_report(member_entries, uploaded_file)
                    st.success("✅ Dữ liệu đã được lưu vào file Time_report.xlsm (bản cập nhật).")

                    st.download_button(
                        label="⬇️ Tải file Time_report đã cập nhật",
                        data=updated_file,
                        file_name="Time_report_updated.xlsm",
                        mime="application/vnd.ms-excel.sheet.macroEnabled.12"
                    )
                except Exception as e:
                    st.error(f"❌ Lỗi khi lưu dữ liệu: {e}")
            else:
                st.warning("⚠️ Không có thành viên nào được chọn là 'Có mặt'.")
else:
    st.info("Vui lòng upload file Time_report.xlsm để bắt đầu nhập dữ liệu.")
