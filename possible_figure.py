import pandas as pd
import plotly.express as px
import plotly
from main import df2

df2 = df2
df3_cols = df2.columns.values.tolist()
df3_cols = df3_cols[:2]
df3_vals = df2.loc[0]
df3_vals = df3_vals[:2]
df3_vals = df3_vals.tolist()

df3 = pd.DataFrame(list(zip(df3_cols, df3_vals)),
               columns=['Category', 'Amount'])
df3_values = df3['Amount']
df3_names = df3['Category']
print(df3)

