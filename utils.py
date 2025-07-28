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

def save_to_time_report(entries, uploaded_file):
    """
    Save work hour entries to the uploaded Time_report.xlsm file (uploaded via Streamlit).
    Writes to the 'Raw_Data' sheet. Returns a BytesIO Excel file after update.
    """
    if uploaded_file is None:
        raise ValueError("Chưa upload file Time_report.xlsm.")

    # Convert list of dict to DataFrame
    df = pd.DataFrame(entries)

    # Đọc nội dung file upload vào memory buffer
    in_memory = BytesIO(uploaded_file.read())

    # Load workbook từ memory, giữ macro
    wb = load_workbook(filename=in_memory, keep_vba=True)

    # Nếu chưa có sheet 'Raw_Data' thì tạo mới
    if 'Raw_Data' not in wb.sheetnames:
        ws = wb.create_sheet("Raw_Data")
        ws.append(df.columns.tolist())
    else:
        ws = wb["Raw_Data"]

    # Append vào cuối sheet
    for row in dataframe_to_rows(df, index=False, header=False):
        ws.append(row)

    # Save lại workbook vào memory buffer mới
    out_memory = BytesIO()
    wb.save(out_memory)
    out_memory.seek(0)
    return out_memory  # trả về file để cho phép user tải xuống
