import streamlit as st
import pandas as pd
from datetime import datetime
from utils import (
    load_team_config, load_project_config, load_job_config,
    get_team_members, append_to_time_report, check_team_completion
)

st.set_page_config(page_title="Nhập dữ liệu nhóm", layout="wide")

st.title("📋 Nhập Dữ Liệu Làm Việc Theo Nhóm")

# Load config files
team_df = load_team_config()
project_df = load_project_config()
job_df = load_job_config()

# Chọn ngày làm việc
selected_date = st.date_input("🗓️ Ngày làm việc", value=datetime.today())

# Chọn nhóm trưởng (đúng cột là 'Group Leader')
team_leaders = team_df['Group Leader'].dropna().unique().tolist()
selected_leader = st.selectbox("👤 Chọn nhóm trưởng", team_leaders)

if selected_leader:
    members = get_team_members(team_df, selected_leader)
    with st.form("data_entry_form", clear_on_submit=True):
        st.write(f"### 👥 Thành viên nhóm: {selected_leader}")
        rows = []
        for member in members:
            st.markdown(f"#### 🧑‍💼 {member}")
            project = st.selectbox(f"  • Dự án ({member})", project_df['Tên dự án'], key=f'project_{member}')
            job = st.selectbox(f"  • Công việc ({member})", job_df['Tên công việc'], key=f'job_{member}')
            hours = st.number_input(f"  • Giờ làm ({member})", min_value=0.0, max_value=24.0, value=8.0, step=0.5, key=f'hours_{member}')
            rows.append({
                'Ngày làm': selected_date,
                'Nhóm trưởng': selected_leader,
                'Tên nhân sự': member,
                'Dự án': project,
                'Công việc': job,
                'Số giờ': hours
            })

        submitted = st.form_submit_button("💾 Ghi dữ liệu")
        if submitted:
            df_new = pd.DataFrame(rows)
            try:
                append_to_time_report(df_new)
                st.success("✅ Đã lưu dữ liệu vào Time_report.xlsm")
            except Exception as e:
                st.error(f"❌ Lỗi khi lưu: {e}")

# Kiểm tra nhóm nào nhập đủ/chưa đủ
st.divider()
st.subheader("📊 Kiểm tra tình trạng nhập dữ liệu")

if st.button("🔍 Kiểm tra nhóm"):
    try:
        raw_df = pd.read_excel("Time_report.xlsm", sheet_name="Raw_Data")
        status_df = check_team_completion(raw_df, selected_date, team_df)
        st.dataframe(status_df)
    except Exception as e:
        st.error(f"Không đọc được dữ liệu: {e}")
