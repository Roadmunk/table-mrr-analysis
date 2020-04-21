import pandas as pd
from datetime import datetime as dt

# This file contains all of the accounts' MRR as they are provided by the input system.
df = pd.read_csv('schema/mrr_raw/Mar-2020 Data.csv')
num = df._get_numeric_data()
num[num < 0] = 0

# Identify subscriptions WITH an 'N/A' in any cell and write them to a file with a datetime suffix.
error_df = df.loc[df.isna().any(axis=1)]
error_path = "schema/mrr_errors/mrr_errors_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
error_df.to_csv(error_path, index=False)

# Identify subscriptions WITHOUT an 'N/A' in any cell and write them to a file with a datetime suffix.
df_for_processing = df.loc[df.notna().all(axis=1)]
clean_path = "schema/mrr_clean/mrr_clean_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
df_for_processing.to_csv(clean_path, index=False)

print(error_df, df_for_processing)