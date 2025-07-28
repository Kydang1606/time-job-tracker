# utils.py
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def load_excel_config(filepath):
    try:
        return pd.read_excel(filepath)
    except Exception as e:
        st.error(f"❌ Error loading config file {filepath}: {e}")
        return pd.DataFrame()

def filter_data_by_config(mode, project_df, team_df, job_df):
    if mode == "Compare Projects in a Month":
        selected_month = st.selectbox("Select Month", sorted(project_df['Month'].dropna().unique()))
        selected_projects = st.multiselect("Select Projects", sorted(project_df['Project'].dropna().unique()))
        if selected_month and selected_projects:
            return {
                "month": selected_month,
                "projects": selected_projects
            }
    elif mode == "Compare Projects Over Time":
        selected_years = st.multiselect("Select Year(s)", sorted(project_df['Year'].dropna().unique()))
        selected_projects = st.multiselect("Select Projects", sorted(project_df['Project'].dropna().unique()))
        if selected_years and selected_projects:
            return {
                "years": selected_years,
                "projects": selected_projects
            }
    return None

def show_comparison_chart(df, config, mode):
    if mode == "Compare Projects in a Month":
        month = config['month']
        projects = config['projects']
        filtered = df[(df['Month'] == month) & (df['Project'].isin(projects))]
        summary = filtered.groupby('Project')['Hours'].sum().reset_index()
    else:
        years = config['years']
        projects = config['projects']
        filtered = df[(df['Year'].isin(years)) & (df['Project'].isin(projects))]
        summary = filtered.groupby(['Year', 'Project'])['Hours'].sum().reset_index()

    if summary.empty:
        st.warning("No data matches your filter.")
        return

    fig = plt.figure(figsize=(10, 5))
    if mode == "Compare Projects in a Month":
        sns.barplot(data=summary, x='Project', y='Hours')
        plt.title(f'Project Hours in {month}')
    else:
        sns.barplot(data=summary, x='Year', y='Hours', hue='Project')
        plt.title(f'Project Hours Over Time')

    st.pyplot(fig)
