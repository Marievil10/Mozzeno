# packages used for the connection between the script and the Google sheet
from credentials_file import get_credentials
from functions import get_max_mozzeno_file, delete_file
# packages used for the dataframes
import pandas as pd
from datetime import date
import gspread_dataframe
from fixed_values import df_percent
# received a Future Warning
pd.set_option('future.no_silent_downcasting', True)

# connecting to the correct file
sheet = get_credentials('Revolut & Degiro', 'Mozzeno')
# sheet = get_credentials('Test_connection_sheets', 'Marie')

# finding the correct file in the download folder
folder_path = r'/Users/marieperin/Downloads'
file_type = r'/*xlsx'
max_file = get_max_mozzeno_file(folder_path, file_type)
df_file = pd.read_excel(max_file)

# creation of the information dataframe
df = df_file.copy()
df = df[['Lening toegekend op', 'Uw inschrijving', 'Terugbetaald kapitaal',
         'Rente', 'Vooruitgang', 'Looptijd', 'Status']]
df = df.rename(columns={'Lening toegekend op': 'Renewal date', 'Uw inschrijving': 'Invested',
                        'Terugbetaald kapitaal': 'Paid back', 'Rente': 'Interest'})
df['Remaining'] = df['Invested'] - df['Paid back']
df['Remaining months'] = df['Looptijd'] - df['Vooruitgang']
df['Renewal date'] = pd.to_datetime(df['Renewal date'], dayfirst=True)
df['Fully paid back'] = ((df['Renewal date'].dt.to_period('M')) + df['Remaining months']).dt.to_timestamp()
df['Fully paid back'] = df['Fully paid back'].dt.date
df['Renewal date'] = df['Renewal date'].dt.date
df = df.drop(['Looptijd', 'Vooruitgang', 'Remaining months'], axis=1)

# fixed values because they are in the past or not mine
bonus_received = 4.9
gain_2023 = 8.14

# calculations
cell = sheet.find('Start capital')  # can be that the lay out of the sheet changes, so no fixed field
if cell is None:
    start_capital = 500.00
else:
    start_capital = int(sheet.cell(cell.row + 1, cell.col).value)

# did_you_deposit_extra = input('Did your invested money change (deposit/withdraw)? Y/N ')
# if did_you_deposit_extra == 'Y':
#     deposit_how_much = int(input('With much? '))
#     start_capital += deposit_how_much
# else:
#     start_capital = start_capital

value_nodes = df['Invested'].sum()
value_back = df['Paid back'].sum()
value_interest = df['Interest'].sum()
value_remaining = df['Remaining'].sum()
total_gain = bonus_received + value_interest
gain_2024 = total_gain - gain_2023
gain_percentage = float(total_gain / start_capital)
available_amount = round(start_capital - value_remaining + total_gain, 2)
worth_portfolio = start_capital + total_gain

replacers = {'Op tijd': 1, 'Vervroegde terugbetaling': 2}
df['Status'] = df['Status'].replace(replacers)

# some fillers
status_text = 'Panic'
for x in df['Status']:
    if x in range(1, 3):
        status_text = 'Good'
latest_paid_back = max(df['Fully paid back'])
first_invested = date(2023, 8, 29).strftime('%d/%m/%Y')

# filling in the information dataframe, starting with the totals within the  cells
# in the first line in the sheet
df = df[['Renewal date', 'Invested', 'Paid back', 'Interest',
         'Remaining', 'Status', 'Fully paid back']]
df.loc[-1] = [first_invested, value_nodes, value_back, value_interest,
              value_remaining, status_text, latest_paid_back]
df.index = df.index + 1
df.sort_index(inplace=True)
end_of_info_df_right = df.shape[1]
end_of_info_df_bottom = df.shape[0]

# construction of the general dataframe, placed two columns next to the information dataframe
today = date.today().strftime('%d/%m/%Y')
df2 = pd.DataFrame(columns=['Start capital', 'Gain', 'Current worth',
                            'Available', 'Gain percentage', 'Last updated'])
df2.loc[0] = [start_capital, total_gain, worth_portfolio,
              available_amount, gain_percentage, today]
start_of_general_df = end_of_info_df_right + 2

# construction of the estimation dataframe, placed two rows below the information dataframe
df3 = df_file.copy()
df3 = df3[['Uw inschrijving', 'Rentevoet van de serie', 'Status', 'Rente']]
df3['Status'] = df3['Status'].replace(replacers)

df3 = df3.rename(columns={'Uw inschrijving': 'Node value', 'Rentevoet van de serie': 'Bruto'})
df3 = df3[df3['Status'] == 1]
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
df3[''], df3['2024 gain'] = ['', '']
df3.loc[df3.index[-1], '2024 gain'] = total_gain - gain_2023
df3 = df3.drop(['Rente', 'Status'], axis=1)
df3 = df3.drop(df3.index[0:df3.shape[0] - 1])
start_of_est_df = end_of_info_df_bottom + 3

# the actual updating of the Google sheet
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
