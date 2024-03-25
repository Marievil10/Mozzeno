import gspread_dataframe
from credentials_file import get_credentials
from main import df
from informative_dataframe import df, start_of_general_df

sheet = get_credentials('Revolut & Degiro', 'Mozzeno')

# the actual updating of the Google sheet
gspread_dataframe.set_with_dataframe(worksheet=sheet,
                                     dataframe=df,
                                     include_column_header=True)

gspread_dataframe.set_with_dataframe(worksheet=sheet,
                                     dataframe=df2,
                                     col=start_of_general_df,
                                     include_column_header=True)