# utils.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_excel_config(path):
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        st.error(f"Failed to load config: {e}")
        return pd.DataFrame()

def filter_data_by_config(mode, project_df, team_df, job_df):
    config = {}
    if project_df.empty or team_df.empty or job_df.empty:
        st.warning("⚠️ One or more config files are missing or empty.")
        return None

    member_list = team_df['Thành viên'].dropna().tolist()
    config["members"] = member_list
    config["selected_projects"] = {}
    config["selected_jobs"] = {}

    if mode == "Compare Projects in a Month":
        year = st.selectbox("Năm", [2023, 2024, 2025])
        month = st.selectbox("Tháng", list(range(1, 13)))
        config["year"] = year
        config["months"] = [month]

    else:  # "Compare Projects Over Time"
        year_options = [2023, 2024, 2025]
        selected_years = st.multiselect("Chọn năm", year_options, default=[2024])
        config["years"] = selected_years
        config["months"] = []

    for member in member_list:
        with st.expander(f"🧑 Cấu hình cho {member}"):
            member_projects = project_df[project_df['Thành viên'] == member]['Tên dự án'].dropna().unique().tolist()
            selected_projects = st.multiselect(f"  • Dự án ({member})", member_projects, key=f'project_{member}')
            config["selected_projects"][member] = selected_projects

            member_jobs = job_df[job_df['Thành viên'] == member]['Công việc'].dropna().unique().tolist()
            selected_jobs = st.multiselect(f"  • Công việc ({member})", member_jobs, key=f'job_{member}')
            config["selected_jobs"][member] = selected_jobs

    return config

def show_comparison_chart(raw_df, config, mode):
    if 'Ngày' not in raw_df.columns or 'Thành viên' not in raw_df.columns:
        st.error("❌ Raw data must contain columns: 'Ngày', 'Thành viên', 'Tên dự án', 'Công việc', 'Số giờ'")
        return

    raw_df['Ngày'] = pd.to_datetime(raw_df['Ngày'], errors='coerce')
    raw_df.dropna(subset=['Ngày'], inplace=True)
    raw_df['Tháng'] = raw_df['Ngày'].dt.month
    raw_df['Năm'] = raw_df['Ngày'].dt.year

    df = pd.DataFrame()

    for member in config['members']:
        df_member = raw_df[raw_df['Thành viên'] == member]

        if mode == "Compare Projects in a Month":
            df_member = df_member[
                (df_member['Năm'] == config['year']) & 
                (df_member['Tháng'].isin(config['months']))
            ]
        else:
            df_member = df_member[
                df_member['Năm'].isin(config.get('years', []))
            ]

        if member in config['selected_projects']:
            df_member = df_member[df_member['Tên dự án'].isin(config['selected_projects'][member])]
        if member in config['selected_jobs']:
            df_member = df_member[df_member['Công việc'].isin(config['selected_jobs'][member])]

        df = pd.concat([df, df_member], ignore_index=True)

    if df.empty:
        st.warning("⚠️ No data matched the current filters.")
        return

    agg_column = 'Tháng' if mode == "Compare Projects in a Month" else 'Năm'

    chart_data = df.groupby(['Tên dự án', agg_column])['Số giờ'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=chart_data, x=agg_column, y='Số giờ', hue='Tên dự án', ax=ax)
    ax.set_title("So sánh thời gian các dự án")
    ax.set_ylabel("Tổng số giờ")
    st.pyplot(fig)
