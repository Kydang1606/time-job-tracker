# app.py
import streamlit as st
import pandas as pd
from utils import (
    load_excel_config,
    save_time_entry,
    get_all_entries
)

st.set_page_config(page_title="Nhập dữ liệu thời gian làm việc", layout="wide")
st.title("📝 Nhập dữ liệu thời gian làm việc")

# --- Load configs ---
project_df = load_excel_config("Project_Config.xlsx")
team_df = load_excel_config("Team_Config.xlsx")
job_df = load_excel_config("Job_Config.xlsx")

# --- Form nhập liệu ---
with st.form("time_entry_form"):
    st.subheader("➕ Nhập thông tin thời gian làm việc")

    employee = st.selectbox("👤 Nhân viên", team_df["Employee"].unique())
    project = st.selectbox("📁 Dự án", project_df["Project"].unique())
    job = st.selectbox("🧩 Công việc", job_df["Job"].unique())
    work_date = st.date_input("📅 Ngày làm việc")
    hours = st.number_input("⏱️ Số giờ làm", min_value=0.0, step=0.5)

    submitted = st.form_submit_button("💾 Lưu dữ liệu")

    if submitted:
        save_time_entry(employee, project, job, work_date, hours)
        st.success("✅ Dữ liệu đã được lưu thành công.")

# --- Hiển thị dữ liệu đã nhập ---
st.subheader("📋 Dữ liệu đã nhập")
entries_df = get_all_entries()
if not entries_df.empty:
    st.dataframe(entries_df)
else:
    st.info("Chưa có dữ liệu.")
