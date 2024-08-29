# packages used for the connection between the script and the Google sheet
from credentials_file import get_credentials
from functions import get_max_mozzeno_file, delete_file, status_payment
# packages used for the dataframes
import pandas as pd
from datetime import date
import gspread_dataframe
from fixed_values import df_percent, start_capital, bonus_received, gain_2023

# received a Future Warning
pd.set_option('future.no_silent_downcasting', True)

# connecting to the correct file
sheet = get_credentials('name of file', 'name of sheet')

# a check to see if Withdrawn is already filled in, basically to see if the sheet
# has already been filled in general, or the script has already been used
cell = sheet.find('Withdrawn')
if cell is None:
    withdrawn = 0.00
else:
    original_withdrawn = sheet.cell(cell.row + 1, cell.col).value
    if original_withdrawn is None:
        withdrawn = 0.00
    else:
        did_you_deposit_extra = input('Did your invested money change (deposit/withdraw)? Y/N ')
        original_withdrawn = float(original_withdrawn.replace(',', '.').strip())
        if did_you_deposit_extra == 'Y':
            change_how_much = float(input('With much? '))
            withdrawn = original_withdrawn + change_how_much
        else:
            withdrawn = original_withdrawn

# finding the correct file in the download folder
folder_path = r'your_path'
file_type = r'/*xlsx'
max_file = get_max_mozzeno_file(folder_path, file_type)
df_file = pd.read_excel(max_file)
sheet.clear()

# creation of all the dataframes based on the csv-file (Dutch)
df = df_file.copy()
df = df[['Lening toegekend op', 'Uw inschrijving', 'Terugbetaald kapitaal',
         'Rente', 'Vooruitgang', 'Looptijd', 'Status']]
df = df.rename(columns={'Lening toegekend op': 'Renewal date', 'Uw inschrijving': 'Invested',
                        'Terugbetaald kapitaal': 'Paid back', 'Rente': 'Interest'})

df2 = pd.DataFrame(columns=['Start capital', 'Gain', 'Current worth',
                            'Available', 'Gain percentage', 'Last updated',
                            'Withdrawn'])

df3 = df_file.copy()
df3 = df3[['Uw inschrijving', 'Rentevoet van de serie', 'Status', 'Rente']]
df3 = df3.rename(columns={'Uw inschrijving': 'Node value', 'Rentevoet van de serie': 'Bruto'})

# defining the edges of the dataframes as references for other dataframes
end_of_info_df_right = df.shape[1]
end_of_info_df_bottom = df.shape[0]
start_of_general_df = end_of_info_df_right + 2
start_of_est_df = end_of_info_df_bottom + 4

# fixed values because they are in the past or not mine
first_invested_date = date(2023, 8, 29).strftime('%d/%m/%Y')
today = date.today().strftime('%d/%m/%Y')

# filling in df
# doing some transformations based on the information in the csv
df['Status'] = status_payment(df['Status'])
df['Remaining'] = df['Invested'] - df['Paid back']
df['Remaining months'] = df['Looptijd'] - df['Vooruitgang']
df['Renewal date'] = pd.to_datetime(df['Renewal date'], dayfirst=True)
df['Fully paid back'] = ((df['Renewal date'].dt.to_period('M')) + df['Remaining months']).dt.to_timestamp()
df['Fully paid back'] = df['Fully paid back'].dt.date
df['Renewal date'] = df['Renewal date'].dt.date
df = df.drop(['Looptijd', 'Vooruitgang', 'Remaining months'], axis=1)

# some summary fields
value_nodes = df['Invested'].sum()
value_back = df['Paid back'].sum()
value_interest = df['Interest'].sum()
value_remaining = df['Remaining'].sum()

# in case there is a payment overdue, we will have the status 'panic'
status_text = 'Good'
unique_values = df.Status.unique()
if 4 in unique_values:
    status_text = 'Panic'
else:
    if 3 in unique_values:
        status_text = 'Anticipating'

# the last ever date you receive a payment
latest_paid_back = max(df['Fully paid back'])

# filling all the summaries in the second row of the sheet
df.loc[-1] = [first_invested_date, value_nodes, value_back, value_interest,
              status_text, value_remaining, latest_paid_back]
df.index = df.index + 1
df.sort_index(inplace=True)

# filling in df3
# filtering on only the ongoing, on time payments, as they are the most certain
df3['Status'] = status_payment(df3['Status'])
status_options = [1, 3, 4]
df3 = df3[df3['Status'].isin(status_options)]
df3['Bruto'] = round(df3['Bruto'], 2)
df3 = pd.merge(df3, df_percent, on='Bruto')
df3['Total projected gain'] = round(df3['Node value'] * df3['Netto'] / 100, 2)

# getting the totals and averages
df3.loc[df3.index[-1], 'Node value'] = df3['Node value'].sum()
df3.loc[df3.index[-1], 'Total projected gain'] = df3['Total projected gain'].sum()
df3.loc[df3.index[-1], 'Rente'] = df3['Rente'].sum()
df3.loc[df3.index[-1], 'Bruto'] = df3['Bruto'].mean() / 100
df3.loc[df3.index[-1], 'Netto'] = df3['Netto'].mean() / 100
df3['Remaining gain'] = df3['Total projected gain'] - df3['Rente']

# leaving an empty column so the current year's gain has its separate field
df3[''], df3['2024 gain'] = ['', '']
total_gain = bonus_received + value_interest
df3.loc[df3.index[-1], '2024 gain'] = total_gain - gain_2023
df3 = df3.drop(['Rente', 'Status'], axis=1)
df3 = df3.drop(df3.index[0:df3.shape[0] - 1])

# filling in df2
gain_percentage = total_gain / start_capital
worth_portfolio = round(start_capital + total_gain - withdrawn, 2)
available_amount = round(start_capital - value_remaining + total_gain - withdrawn, 2)
df2.loc[0] = [start_capital, total_gain, worth_portfolio,
              available_amount, gain_percentage, today, withdrawn]

gspread_dataframe.set_with_dataframe(worksheet=sheet,
                                     dataframe=df,
                                     include_column_header=True)

gspread_dataframe.set_with_dataframe(worksheet=sheet,
                                     dataframe=df2,
                                     col=start_of_general_df,
                                     include_column_header=True)

gspread_dataframe.set_with_dataframe(worksheet=sheet,
                                     dataframe=df3,
                                     row=start_of_est_df,
                                     include_column_header=True)

# deletion of the file to not overcrowd my downloads file
delete_file(max_file)
