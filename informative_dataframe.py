import pandas as pd
from functions import get_max_mozzeno_file
from datetime import date
from fixed_values import bonus_received, gain_2023, start_capital

folder_path = r'/Users/marieperin/Downloads'
file_type = r'/*xlsx'
max_file = get_max_mozzeno_file(folder_path, file_type)

df = pd.read_excel(max_file)
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

start_capital = start_capital

did_you_deposit_extra = input('Did your invested money change (deposit/withdraw)? Y/N ')
if did_you_deposit_extra == 'Y':
    deposit_how_much = int(input('With much? '))
    start_capital += deposit_how_much
else:
    start_capital = start_capital

value_nodes = df['Invested'].sum()
value_back = df['Paid back'].sum()
value_interest = df['Interest'].sum()
value_remaining = df['Remaining'].sum()
total_gain = bonus_received + value_interest
gain_2024 = total_gain - gain_2023
gain_percentage = float(total_gain / start_capital)
available_amount = round(start_capital - value_remaining + total_gain, 2)
worth_portfolio = start_capital + total_gain

df['Status'] = df['Status'].replace('Op tijd', 1)
df['Status'] = df['Status'].replace('Vervroegde terugbetaling', 2)

# some fillers
status_text = 'Too late'
for x in df['Status']:
    if x in range(1, 3):
        status_text = 'Good'
latest_paid_back = max(df['Fully paid back'])
first_invested = date(2023, 8, 29).strftime('%d/%m/%Y')

df = df[['Renewal date', 'Invested', 'Paid back', 'Interest',
         'Remaining', 'Status', 'Fully paid back']]
df.loc[-1] = [first_invested, value_nodes, value_back, value_interest,
              value_remaining, status_text, latest_paid_back]
df.index = df.index + 1
df.sort_index(inplace=True)
