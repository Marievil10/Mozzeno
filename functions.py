from datetime import timedelta
import datetime as dt
import glob
import os

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def get_max_mozzeno_file(folder_path, file_type):
    folder_path = folder_path
    file_type = file_type
    files = glob.glob(folder_path + file_type)
    mozzeno_file_list = []
    for item in files:
        if 'notes' in item:
            mozzeno_file_list.append(item)
    max_file = max(mozzeno_file_list, key=os.path.getctime)
    return max_file

def delete_file(max_file):
    max_file = max_file
    if os.path.isfile(max_file):
        os.remove(max_file)
        print('Successfully deleted')
    else:
        print('Not deleted')

def can_we_delete(max_file):
    max_file = max_file
    today = dt.date.today()
    year = str(today.year)
    start_pos_date = max_file.find(year)
    end_pos_date = start_pos_date + 8
    full_date = max_file[start_pos_date:end_pos_date]
    full_date = dt.datetime.strptime(full_date, '%Y%m%d')
    full_date = full_date.date()
    if today < full_date:
        answer = 'N'
    else:
        answer = 'Y'
    return answer

