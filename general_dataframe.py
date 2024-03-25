from datetime import date
from fixed_values import start_capital
from informative_dataframe import total_gain, worth_portfolio, available_amount, gain_percentage
import pandas as pd

today = date.today().strftime('%d/%m/%Y')
df2 = pd.DataFrame(columns=['Start capital', 'Gain', 'Current worth',
                            'Available', 'Gain percentage', 'Last updated'])
df2.loc[0] = [start_capital, total_gain, worth_portfolio,
              available_amount, gain_percentage, today]
print(df2)