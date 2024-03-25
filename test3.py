import os
import datetime as dt
folder_path = r'/Users/marieperin/Downloads/'
max_file = 'notes_900100001860_20240316_140397.xlsx'

def delete_file(folder_path, max_file):
    folder_path = folder_path
    max_file = max_file
    file_path = str(folder_path + max_file)
    answer = can_we_delete(max_file)
    if answer == 'Y':
        if os.path.isfile(file_path):
            os.remove(file_path)
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


delete_file(folder_path,max_file)