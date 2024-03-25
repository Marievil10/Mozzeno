import pandas as pd
from functions import get_max_mozzeno_file

folder_path = r'/Users/marieperin/Downloads'
file_type = r'/*xlsx'
max_file = get_max_mozzeno_file(folder_path, file_type)

est_bruto = [4.75, 5.05, 5.15, 5.25, 5.35, 5.45, 5.55, 5.65, 5.75, 5.85, 5.95, 6.05]
est_netto = [3.30, 3.51, 3.58, 3.65, 3.72, 3.79, 3.85, 3.92, 4.00, 4.06, 4.13, 4.20]

df_percent = pd.DataFrame(list(zip(est_bruto, est_netto)),
                          columns=['Bruto', 'Netto'])

max_file = get_max_mozzeno_file(folder_path, file_type)
df3 = pd.read_excel(max_file)
df3 = df3[['Uw inschrijving', 'Rentevoet van de serie', 'Status', 'Rente']]
df3 = df3.rename(columns={'Uw inschrijving': 'Invested', 'Rentevoet van de serie': 'Bruto'})

df3['Status'] = df3['Status'].replace('Op tijd', 1)
df3['Status'] = df3['Status'].replace('Vervroegde terugbetaling', 2)

df3['Bruto'] = round(df3['Bruto'], 2)
df3 = df3[df3['Status'] == 1]
df3 = df3.drop('Status', axis=1)
df3 = pd.merge(df3, df_percent, on='Bruto')
df3['Total projected gain'] = round(df3['Invested'] * df3['Netto'] / 100, 2)

df3.loc[df3.index[-1], 'Invested'] = df3['Invested'].sum()
df3.loc[df3.index[-1], 'Bruto'] = df3['Bruto'].mean()
df3.loc[df3.index[-1], 'Netto'] = df3['Netto'].mean()
df3.loc[df3.index[-1], 'Total projected gain'] = df3['Total projected gain'].sum()
df3.loc[df3.index[-1], 'Rente'] = df3['Rente'].sum()
df3['Remaining gain'] = df3['Total projected gain'] - df3['Rente']
df3 = df3.drop('Rente', axis=1)
df3 = df3.drop(df3.index[0:11])

print(df3)
