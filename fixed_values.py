import pandas as pd

# these values are for me personally, feel free to fill in your own
bonus_received = 4.9
gain_2023 = 8.52
start_capital = 500

# acceptated values for language are 'NL' and 'FR', depending on in which language you downloaded your CSV.
language_moz = 'NL'

# these values are from the Mozzeno site
est_bruto = [4.75, 5.05, 5.15, 5.25, 5.35, 5.45, 5.55, 5.65, 5.75, 5.85, 5.95, 6.05, 6.10]
est_netto = [3.30, 3.51, 3.58, 3.65, 3.72, 3.79, 3.85, 3.92, 4.00, 4.06, 4.13, 4.20, 4.23]

df_percent = pd.DataFrame(list(zip(est_bruto, est_netto)),
                          columns=['Bruto', 'Netto'])