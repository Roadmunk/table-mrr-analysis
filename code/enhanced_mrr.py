import pandas as pd
import numpy as np
from datetime import datetime as dt
import glob
import os

# Get all the CSV files in the mrr_clean folder.
list_of_files = glob.glob('schema/mrr_clean/*.csv')
# Pick the most recent one and open it as a Pandas dataframe.
latest_mrr_file = max(list_of_files, key=os.path.getctime)
latest_mrr_df = pd.read_csv(latest_mrr_file)

# Create a cloumn to assign tiers to logos.
# These values are based on annual/12, e.g. $25,000/12 = $2083
def find_four_tier(logo):
    if logo.last_valid_index() is None:
        return np.nan
    else:
        if logo[logo.last_valid_index()] > 2083:
            return 1
        elif logo[logo.last_valid_index()] > 499:
            return 2 
        elif logo[logo.last_valid_index()] > 49:
            return 3
        else:
            return 4
latest_mrr_df['four_tier'] = latest_mrr_df.apply(find_four_tier, axis=1)

# Create a cloumn to assign additional tiers to logos.
def find_two_tier(logo):
    if logo.last_valid_index() is None:
        return np.nan
    else:
        if logo[logo.last_valid_index()] > 499:
            return 'A'
        else:
            return 'B'
latest_mrr_df['two_tier'] = latest_mrr_df.apply(find_two_tier, axis=1)

# Remove text columns so only MRR columns remain.
no_text = latest_mrr_df.drop(['Customer Name', 'four_tier', 'two_tier'], axis=1)
# Sum those columns.
sum_columns = no_text.to_numpy().cumsum(1)
# Find the header of the first column without a zero.
start_column = no_text.columns[(sum_columns!=0).argmax(1)]
# Find the header of the last column without a zero.
end_column = no_text.columns[sum_columns.argmax(1)]
# Assign those headers to the first_date and start_date columns.
latest_mrr_df['first_date'] = start_column
latest_mrr_df['last_date'] = end_column

# Add an analysis_datetime column with the current datetime.
latest_mrr_df['analysis_datetime'] = dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p")

# Remove rows without any MRR (first & last date = '2015-01-31')
latest_mrr_df = latest_mrr_df.drop(latest_mrr_df[(latest_mrr_df.first_date == '2015-01-31') & 
    (latest_mrr_df.last_date == '2015-01-31')].index)

# Output to CSV
latest_enriched_path = "schema/mrr_enriched/mrr_enriched_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
latest_mrr_df.to_csv(latest_enriched_path, index=False)

print(latest_mrr_df)