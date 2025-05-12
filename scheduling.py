from credentials_file import get_credentials
from functions import get_max_mozzeno_file, determine_filedate, first_weekday, run_file
from datetime import datetime
import time

sheet = get_credentials('name of file', 'name of sheet')
folder_path = r'your_path'
file_type = r'/*xlsx'
max_file = get_max_mozzeno_file(folder_path, file_type)
filedate = determine_filedate(max_file)

if __name__ == "__main__":
    last_updated = sheet.find('Last updated')
    cell3 = sheet.cell(last_updated.row + 1, last_updated.col).value
    cell3 = datetime.strptime(cell3, "%d-%m-%Y").date()

    while True:
        if first_weekday():
            if filedate < cell3:
                print(f'{cell3} - File is outdated. Download file again. Retrying tomorrow.')
                time.sleep(86400)
            elif filedate == cell3:
                redo_update = input('You have already updated your sheet today. Are you you want to do it again? Y/N ').strip().upper()
                if redo_update == 'Y':
                    run_file("main.py")
                else:
                    print('Sheet will not be updated.')
                    print('Retrying tomorrow.')
                time.sleep(86400)
            else:
                run_file("run_main_popup.py")
                time.sleep(86400)
        time.sleep(3600)


