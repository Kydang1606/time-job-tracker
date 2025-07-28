import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def load_team_config(file_path='Team_Config.xlsx'):
    df = pd.read_excel(file_path)
    df.dropna(how='all', inplace=True)
    return df

def load_project_config(file_path='Project_Config.xlsx'):
    return pd.read_excel(file_path)

def load_job_config(file_path='Job_Config.xlsx'):
    return pd.read_excel(file_path)

def get_team_members(team_df, team_leader):
    return team_df[team_df['Nhóm trưởng'] == team_leader]['Tên thành viên'].dropna().tolist()

def append_to_time_report(df_to_append, file_path='Time_report.xlsm'):
    book = load_workbook(file_path)
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    
    sheet_name = 'Raw_Data'
    start_row = writer.sheets[sheet_name].max_row + 1
    
    df_to_append.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=start_row)
    writer.save()

def check_team_completion(df_raw, date, team_config):
    expected = team_config.groupby('Nhóm trưởng')['Tên thành viên'].count()
    submitted = df_raw[df_raw['Ngày làm'] == date].groupby('Nhóm trưởng')['Tên nhân sự'].nunique()
    merged = pd.DataFrame({'Đã nhập': submitted, 'Cần nhập': expected})
    merged.fillna(0, inplace=True)
    merged['Còn thiếu'] = merged['Cần nhập'] - merged['Đã nhập']
    return merged.reset_index()
