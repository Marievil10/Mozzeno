import sys
from datetime import timedelta
import datetime as dt
import glob
import os
from fixed_values import language_moz
import subprocess

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
    if not mozzeno_file_list:
        print('No valid Mozzeno file found!')
        sys.exit()
    max_file = max(mozzeno_file_list, key=os.path.getctime)
    return max_file

def delete_file(max_file):
    max_file = max_file
    if os.path.isfile(max_file):
        os.remove(max_file)
        print('New information successfully uploaded.')
        print('File successfully deleted.')
        sys.exit()
    else:
        print('Not deleted')

def status_payment(old_list):
    status_number = []
    if language_moz == 'NL':
        on_time = 'Op tijd'
        was_early = 'terugbetaling'
        promise = 'Betalingsbelofte'
        too_late = 'achterstallig'
    elif language_moz == 'FR':
        on_time = 'jour'
        was_early = 'anticipé'
        promise = 'paiement'
        too_late = 'to be seen'
    for text in old_list:
        if on_time in text:
            new_status = 1
            status_number.append(new_status)
        elif was_early in text:
            new_status = 2
            status_number.append(new_status)
        elif promise in text:
            new_status = 3
            status_number.append(new_status)
        elif too_late in text:
            new_status = 4
            status_number.append(new_status)
        else:
            new_status = 0
            status_number.append(new_status)
    return status_number

def language_mismatch():
    print('Language CSV file and fixed value do not match, please adjust and try again.')
    sys.exit()

def yes_button_clicked(popup_window):
    subprocess.run(["python", "main.py"])
    popup_window.destroy()

def no_button_clicked():
    if language_moz == 'NL':
        no = 'Nee'
        print(f"{no}-knop geklikt. Klik 'Sluiten' om het proces af te sluiten.")
    else:
        no = 'non'
        print(f"Bouton-{no} cliqué. Cliquez sur 'Fermer' pour terminer le processus.")
