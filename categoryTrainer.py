# IMPORTS
import pandas as pd
import numpy as np
import pathlib
import re
import os

# ENGINE
def setup_engine(output_file, reference_file):

    # NOTE: LOAD OUTPUT AND REFERENCE FILES
    df_out = pd.read_csv(output_file, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,9], names=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])
    df_ref = pd.read_csv(reference_file)

    print(df_ref)

    for index, row in df_out.iterrows():
        # NOTE: CLEAN CATEGORY AND VENDOR COLUMNS
        # TODO: Need to make sure not all spaces are removed via regex
        # TODO: Remove *; * can be used later to identify unique/non-unique categorizations
        if pd.isna(df_out.at[index, 'categoryAuto']) == False:
            category_preclean = df_out.at[index, 'categoryAuto']
            category = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', category_preclean).lower()

            vendor_preclean = df_out.at[index, 'vendor']
            vendor = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', vendor_preclean).lower()

            if category in df_ref['Category'].values:
                if vendor not in df_ref.loc[df_ref['Category'] == category, 'Vendor'].values:
                    df_ref.loc[df_ref['Category'] == category, 'Vendor'] += vendor
            else:
                df_ref = pd.concat([df_ref, pd.DataFrame([{'Category': category, 'Vendor': vendor}])], ignore_index=True)


    print(df_ref)
    # print(df_ref.loc[df_ref['Category'] == 'transfer', 'Vendor'].values[0])

    # df_ref.to_csv(reference_file, index=False)

# RUN
## TODO: Can these be done together? output_folder and output_file, etc.
statement_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Statements'

output_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Outputs'
output_file = os.path.join(output_folder, 'output_data_training.csv')

reference_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Reference'
reference_file = os.path.join(reference_folder, 'category_reference.csv')

setup_engine(output_file, reference_file)