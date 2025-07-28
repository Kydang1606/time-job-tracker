import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def load_config(file_path):
    """Load configuration file into DataFrame"""
    return pd.read_excel(file_path)

# =================== TEAM ===================

def get_team_list(team_df):
    return team_df['Group Leader'].dropna().unique().tolist()

def get_team_members(team_df, group_leader):
    members = team_df[team_df['Group Leader'] == group_leader]['Employee Name']
    return members.dropna().unique().tolist()

def get_employee_id(team_df, employee_name):
    match = team_df[team_df['Employee Name'] == employee_name]
    if not match.empty:
        return match.iloc[0]['Employee ID']
    return "N/A"

# =================== PROJECT ===================

def get_project_list(project_df):
    return project_df['Project Name'].dropna().unique().tolist()

def get_project_code(project_df, project_name):
    match = project_df[project_df['Project Name'] == project_name]
    if not match.empty:
        return match.iloc[0]['Project Code']
    return "N/A"

# =================== JOB ===================

def get_job_list(job_df, selected_project_code_or_name):
    if 'Project Code' in job_df.columns:
        mask = (job_df['Project Code'] == selected_project_code_or_name) | \
               (job_df['Project Name'] == selected_project_code_or_name)
    else:
        mask = job_df['Project Name'] == selected_project_code_or_name
    return job_df[mask]['Job Name'].dropna().unique().tolist()

def get_job_info(job_df, job_name):
    match = job_df[job_df['Job Name'] == job_name]
    if not match.empty:
        row = match.iloc[0]
        return (
            row.get('Job Code', 'N/A'),
            row.get('Workcenter', 'N/A'),
            row.get('Task', 'N/A')
        )
    return ("N/A", "N/A", "N/A")

def save_to_time_report(entries, file_path='Time_report.xlsm', sheet_name='Raw_Data'):
    """
    Append work hour entries to the given Excel macro-enabled file.
    Create file/sheet if not exist. Keeps macros.
    """
    columns = [
        "Date", "Project Name", "Project Code", "Job Name", "Job Code",
        "Employee", "Employee ID", "Team", "Workcenter", "Task", "Hours"
    ]

    # Kiểm tra nếu file chưa tồn tại, tạo mới file và sheet
    if not os.path.exists(file_path):
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name
        ws.append(columns)
        wb.save(file_path)

    # Mở workbook với keep_vba=True giữ macro nếu có
    wb = load_workbook(file_path, keep_vba=True)

    # Tạo sheet nếu chưa có
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
        ws.append(columns)
    else:
        ws = wb[sheet_name]

    # Append dữ liệu
    for entry in entries:
        row = [entry.get(col, "") for col in columns]
        ws.append(row)

    # Lưu workbook
    wb.save(file_path)
    return file_path
