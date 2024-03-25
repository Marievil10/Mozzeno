from datetime import date
import pandas as pd
from functions import last_day_of_month, get_max_mozzeno_file
from main import df2
import calendar

input_date = date.today()
day = input_date.day
month = input_date.month
year = input_date.year
first_day = input_date.replace(day=1)
last_day = last_day_of_month(input_date)

start_value = 9.16
end_value = 0
df_monthly_gain = pd.DataFrame(columns=['Month', 'Gain'])
if input_date == first_day:
    start_value = df2['Gain'].loc[0]
else:
    start_value = start_value

if input_date == last_day:
    end_value = df2['Gain'].loc[0]
    check_end_value = input('Is your end value the same as on Mozzeno? Y/N ')
    if check_end_value == 'N':
        end_value = int(input('Enter correct end value: '))
    else:
        end_value = end_value
    gain_of_month = end_value - start_value
    month = calendar.month_name[month]
    new_row = [month, gain_of_month]
    df_monthly_gain.loc[len(df_monthly_gain)] = new_row
    month = input_date.month


