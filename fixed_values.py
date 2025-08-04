import pandas as pd
import datetime as dt

# these values are for me personally, feel free to fill in your own
bonus_received = 10.42
gain_2023 = 8.52
gain_2024 = 18.49
gain_2025 = 0
today = dt.date.today()
year = str(today.year)
# update every year
gain_years = gain_2023 + gain_2024 + gain_2025
DEFAULT_START_CAPITAL = 500.00

# accepted values for language are 'NL' and 'FR', depending on in which language you downloaded your CSV.
language_moz = 'NL'

column_config = {
    'FR': {
        'df': {
            'columns': [
                'Octroyé le', 'Votre souscription', 'Capital remboursé',
                'Intérêts', 'Progression', 'Durée', 'Statut'
            ],
            'rename': {
                'Octroyé le': 'Renewal date',
                'Votre souscription': 'Invested',
                'Capital remboursé': 'Paid back',
                'Intérêts': 'Interest',
                'Progression': 'Progress',
                'Durée': 'Duration',
                'Statut': 'Status'
            }
        },
        'df3': {
            'columns': [
                'Votre souscription', 'Taux d’intérêt de la série', 'Statut', 'Intérêts', 'Durée'
            ],
            'rename': {
                'Votre souscription': 'Node value',
                'Taux d’intérêt de la série': 'Bruto',
                'Statut': 'Status',
                'Intérêts': 'Interest',
                'Durée': 'Duration'
            }
        }
    },
    'NL': {
        'df': {
            'columns': [
                'Lening toegekend op', 'Uw inschrijving', 'Kapitaal al terugbetaald',
                'Rente', 'Vooruitgang', 'Looptijd', 'Status'
            ],
            'rename': {
                'Lening toegekend op': 'Renewal date',
                'Uw inschrijving': 'Invested',
                'Kapitaal al terugbetaald': 'Paid back',
                'Rente': 'Interest',
                'Vooruitgang': 'Progress',
                'Looptijd': 'Duration',
                'Status': 'Status'
            }
        },
        'df3': {
            'columns': [
                'Uw inschrijving', 'Rentevoet van de serie', 'Status', 'Rente', 'Looptijd'
            ],
            'rename': {
                'Uw inschrijving': 'Node value',
                'Rentevoet van de serie': 'Bruto',
                'Status': 'Status',
                'Rente': 'Interest',
                'Looptijd': 'Duration'
            }
        }
    }
}

# these values are from the Mozzeno site
est_bruto = [4.75, 5.05, 5.15, 5.25, 5.35, 5.45, 5.55, 5.65, 5.75, 5.85, 5.95, 6.05, 6.10]
est_netto = [3.30, 3.51, 3.58, 3.65, 3.72, 3.79, 3.85, 3.92, 4.00, 4.06, 4.13, 4.20, 4.23]

df_percent = pd.DataFrame(list(zip(est_bruto, est_netto)),
                          columns=['Bruto', 'Netto'])
