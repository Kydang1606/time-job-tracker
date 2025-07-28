import pandas as pd
from datetime import datetime
import os

def load_config(file_path):
    """Load configuration file into DataFrame"""
    return pd.read_excel(file_path)

def get_project_list(project_df):
    return project_df['Project Name'].dropna().unique().tolist()

def get_job_list(job_df, selected_project):
    return job_df[job_df['Project Name'] == selected_project]['Job Name'].dropna().unique().tolist()

def get_team_list(team_df):
    return team_df['Person'].dropna().unique().tolist()

def save_daily_log(log_data, save_path='Daily_Log.xlsx'):
    df_new = pd.DataFrame([log_data])

    if os.path.exists(save_path):
        df_existing = pd.read_excel(save_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(save_path, index=False)
    return save_path
