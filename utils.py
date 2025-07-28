import pandas as pd
from datetime import datetime
import os
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def load_config(file_path):
    """Load configuration file into DataFrame"""
    return pd.read_excel(file_path)

# =================== TEAM ===================

def get_team_list(team_df):
    """Lấy danh sách nhóm trưởng"""
    return team_df['Group Leader'].dropna().unique().tolist()

def get_team_members(team_df, group_leader):
    """Lấy danh sách thành viên theo nhóm trưởng"""
    members = team_df[team_df['Group Leader'] == group_leader]['Employee Name']
    return members.dropna().unique().tolist()

def get_employee_id(team_df, employee_name):
    """Trả về mã nhân viên từ tên"""
    match = team_df[team_df['Employee Name'] == employee_name]
    if not match.empty:
        return match.iloc[0]['Employee ID']
    return "N/A"

# =================== PROJECT ===================

def get_project_list(project_df):
    """Lấy danh sách tên dự án"""
    return project_df['Project Name'].dropna().unique().tolist()

def get_project_code(project_df, project_name):
    """Trả về mã dự án từ tên"""
    match = project_df[project_df['Project Name'] == project_name]
    if not match.empty:
        return match.iloc[0]['Project Code']
    return "N/A"

# =================== JOB ===================

def get_job_list(job_df, selected_project_code_or_name):
    """Lọc danh sách công việc theo mã dự án hoặc tên dự án"""
    if 'Project Code' in job_df.columns:
        mask = (job_df['Project Code'] == selected_project_code_or_name) | \
               (job_df['Project Name'] == selected_project_code_or_name)
    else:
        mask = job_df['Project Name'] == selected_project_code_or_name
    return job_df[mask]['Job Name'].dropna().unique().tolist()

def get_job_info(job_df, job_name):
    """Trả về (Job Code, Workcenter, Task) từ Job Name"""
    match = job_df[job_df['Job Name'] == job_name]
    if not match.empty:
        row = match.iloc[0]
        return (
            row.get('Job Code', 'N/A'),
            row.get('Workcenter', 'N/A'),
            row.get('Task', 'N/A')
        )
    return ("N/A", "N/A", "N/A")

def save_to_time_report(entries, report_path="Time_report.xlsm"):
    """
    Save list of work hour entries into an existing Time_report.xlsm file.
    Automatically appends new data into the sheet 'Raw_Data'.
    """
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"File {report_path} chưa tồn tại. Hãy tạo trước hoặc upload lên app.")

    # Convert list of dict to DataFrame
    df = pd.DataFrame(entries)

    # Load the existing Excel workbook
    wb = load_workbook(report_path, keep_vba=True)  # Giữ macro

    # If 'Raw_Data' sheet doesn't exist, create it
    if 'Raw_Data' not in wb.sheetnames:
        ws = wb.create_sheet("Raw_Data")
        ws.append(df.columns.tolist())
    else:
        ws = wb["Raw_Data"]

    # Find the first empty row (sau cùng)
    start_row = ws.max_row + 1 if ws.max_row > 1 else 2

    # Append new data
    for row in dataframe_to_rows(df, index=False, header=False):
        ws.append(row)

    # Save the workbook back (macro-safe)
    wb.save(report_path)
