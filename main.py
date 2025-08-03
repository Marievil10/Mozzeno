# packages used for the connection between the script and the Google sheet
from functions import delete_file, status_payment, get_float_from_cell, update_amount_if_needed
from scheduling import max_file, sheet

# packages used for the dataframes
import pandas as pd
from datetime import date
import gspread_dataframe
from fixed_values import df_percent, bonus_received, gain_years, DEFAULT_START_CAPITAL, language_moz, year

# received a Future Warning
pd.set_option('future.no_silent_downcasting', True)

# a check to see if Withdrawn is already filled in, basically to see if the sheet
# has already been filled in general, or the script has already been used
money_action = input('Did you withdraw or deposit money? Y/N ').strip().upper()
withdrawn = get_float_from_cell(sheet, 'Withdrawn')
start_capital = get_float_from_cell(sheet, 'Start capital')
if start_capital is None or 0:
    start_capital = DEFAULT_START_CAPITAL

if money_action == 'Y':
    withdrawn = update_amount_if_needed(withdrawn, 'withdraw')
    start_capital = update_amount_if_needed(start_capital, 'deposit')

# finding the correct file in the download folder
df_file = pd.read_excel(max_file)
sheet.clear()

# creation of all the dataframes based on the csv-file
df = df_file.copy()
df3 = df_file.copy()

if language_moz == 'FR':
    try:
        df = df[['Octroyé le', 'Votre souscription', 'Capital remboursé',
                 'Intérêts', 'Progression', 'Durée', 'Statut']]
        df = df.rename(columns={'Octroyé le': 'Renewal date', 'Votre souscription': 'Invested',
                                'Capital remboursé': 'Paid back', 'Intérêts': 'Interest', 'Progression': 'Progress',
                                'Durée': 'Duration', 'Statut': 'Status'})
        df3 = df3[['Votre souscription', 'Taux d’intérêt de la série', 'Statut', 'Intérêts', 'Durée']]
        df3 = df3.rename(columns={'Votre souscription': 'Node value', 'Taux d’intérêt de la série': 'Bruto',
                                  'Statut': 'Status', 'Intérêts': 'Interest', 'Durée': 'Duration'})
    except KeyError as e:
        print(e)
else:
    try:
        df = df[['Lening toegekend op', 'Uw inschrijving', 'Kapitaal al terugbetaald',
                 'Rente', 'Vooruitgang', 'Looptijd', 'Status']]
        df = df.rename(columns={'Lening toegekend op': 'Renewal date', 'Uw inschrijving': 'Invested',
                                'Kapitaal al terugbetaald': 'Paid back', 'Rente': 'Interest', 'Vooruitgang': 'Progress',
                                'Looptijd': 'Duration'})
        df3 = df3[['Uw inschrijving', 'Rentevoet van de serie', 'Status', 'Rente', 'Looptijd']]
        df3 = df3.rename(columns={'Uw inschrijving': 'Node value', 'Rentevoet van de serie': 'Bruto',
                                  'Rente': 'Interest', 'Looptijd': 'Duration'})
    except KeyError as e:
        print(e)

df2 = pd.DataFrame(columns=['Start capital', 'Gain', 'Current worth',
                            'Available', 'Gain percentage', 'Last updated',
                            'Withdrawn'])

# fixed values because they are in the past or not mine
first_invested_date = date(2023, 8, 29).strftime('%d/%m/%Y')
today = date.today().strftime('%d/%m/%Y')

# filling in df
# doing some transformations based on the information in the csv
df['Status'] = status_payment(df['Status'])
df['Remaining'] = df['Invested'] - df['Paid back']
df['Renewal date'] = pd.to_datetime(df['Renewal date'], dayfirst=True)
df['Fully paid back'] = ((df['Renewal date'].dt.to_period('M')) + df['Duration']).dt.to_timestamp()
df['Fully paid back'] = df['Fully paid back'].dt.date
df['Renewal date'] = df['Renewal date'].dt.date
df = df.drop(['Duration', 'Progress'], axis=1)

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
elif 3 in unique_values:
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
status_options = [0, 1, 3, 4]
df3 = df3[df3['Status'].isin(status_options)]
df3['Bruto'] = round(df3['Bruto'], 2)
df3 = pd.merge(df3, df_percent, on='Bruto')
df3['Duration'] = df3['Duration'] / 12
df3['Factor'] = df3['Duration'] * df3['Netto'] / 100 + 1
df3['Total projected gain'] = round(df3['Node value'] * df3['Factor'] - df3['Node value'], 2)

# getting the totals and averages
df3.loc[df3.index[-1], 'Node value'] = df3['Node value'].sum()
df3.loc[df3.index[-1], 'Total projected gain'] = df3['Total projected gain'].sum()
df3.loc[df3.index[-1], 'Interest'] = df3['Interest'].sum()
df3.loc[df3.index[-1], 'Bruto'] = df3['Bruto'].mean() / 100
df3.loc[df3.index[-1], 'Netto'] = df3['Netto'].mean() / 100
df3['Remaining gain'] = df3['Total projected gain'] - df3['Interest']

# leaving an empty column so the current year's gain has its separate field
df3[''] = None
gain_column_name = year + ' gain'
df3[gain_column_name] = None
total_gain = bonus_received + value_interest
df3.loc[df3.index[-1], gain_column_name] = total_gain - gain_years
df3 = df3.drop(['Interest', 'Status', 'Factor', 'Duration'], axis=1)
df3 = df3.drop(df3.index[0:df3.shape[0] - 1])

# filling in df2
gain_percentage = total_gain / start_capital
worth_portfolio = round(start_capital + total_gain - withdrawn, 2)
available_amount = round(start_capital - value_remaining + total_gain - withdrawn, 2)
df2.loc[0] = [start_capital, total_gain, worth_portfolio,
              available_amount, gain_percentage, today, withdrawn]

df = df[~df["Status"].isin([2])]

# defining the edges of the dataframes as references for other dataframes
end_of_info_df_right = df.shape[1]  # columns
end_of_info_df_bottom = df.shape[0] # rows
start_of_general_df = end_of_info_df_right + 2
start_of_est_df = end_of_info_df_bottom + 3

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
