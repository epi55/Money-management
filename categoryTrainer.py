import pandas as pd
import pathlib
import re
import os

# ENGINE
def setup_engine(output_file, reference_file):

    # NOTE: LOAD OUTPUT AND REFERENCE FILES
    df_out = pd.read_csv(output_file, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,9], names=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])
    df_ref = pd.read_csv(reference_file)

    for index, row in df_out.iterrows():
        # NOTE: CLEAN CATEGORY AND VENDOR COLUMNS
        if pd.isna(df_out.at[index, 'categoryAuto']) == False:
            pattern = r'\W' # Any one non-word character
            pattern2 = r'\s+' # Any one (or more) spaces
            
            category_preclean = df_out.at[index, 'categoryAuto']
            category = re.sub(pattern, ' ', category_preclean).lower()
            category = re.sub(pattern2, ' ', category)
            
            vendor_preclean = df_out.at[index, 'vendor']
            vendor = re.sub(pattern, ' ', vendor_preclean).lower()
            vendor = re.sub(pattern2, ' ', vendor)

            df_ref.loc[len(df_ref)] = [category, vendor] # Add a new row with len()

    df_ref_grouped = df_ref.groupby('Category')['Vendor'].apply(lambda x: set(x)).reset_index() # Makes a set, managing duplicates
    # df_ref_grouped = df_ref.groupby('Category')['Vendor'].agg(list).reset_index() # Makes a list, not managing duplicates
    df_ref_grouped.to_csv(reference_file, index=False)
    # print(df_ref_grouped) # TEST
    print("Complete.")

# RUN
## TODO: Can these be done together? output_folder and output_file, etc.
statement_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Statements'

output_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Outputs'
output_file = os.path.join(output_folder, 'output_data_training.csv')

reference_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Reference'
reference_file = os.path.join(reference_folder, 'category_reference.csv')

setup_engine(output_file, reference_file)