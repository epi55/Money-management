# IMPORTS
import pandas as pd
import numpy as np
import pathlib
import re
import os

# ENGINE
def setup_engine(output_file, reference_file):

    # NOTE: LOAD OUTPUT AND REFERENCE FILES
    df_output_file = pd.read_csv(output_file, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,9], names=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])
    df_reference_file = pd.read_csv(reference_file)

    print(df_reference_file)

    for index, row in df_output_file.iterrows():
        # NOTE: CLEAN CATEGORY AND VENDOR COLUMNS
        if pd.isna(df_output_file.at[index, 'categoryAuto']) == False:
            category_preclean = df_output_file.at[index, 'categoryAuto']
            category_postclean = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', category_preclean).lower()

            vendor_preclean = df_output_file.at[index, 'vendor']
            vendor_postclean = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', vendor_preclean).lower()

            if category_postclean in df_reference_file['Category'].values:
                if vendor_postclean in df_reference_file.loc[df_reference_file['Category'] == category_postclean, 'Vendor'].values[0]:
                    pass
                else:
                    df_reference_file.loc[df_reference_file['Category'] == category_postclean, 'Vendor'] += [[vendor_postclean]]
            else:
                df_reference_file = pd.concat([df_reference_file, pd.DataFrame([{'Category': category_postclean, 'Vendor': [[vendor_postclean]]}])], ignore_index=True)

    print(df_reference_file)

    # df_reference_file.to_csv(reference_file, index=False)

# RUN
## TODO: Can these be done together? output_folder and output_file, etc.
statement_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Statements'

output_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Outputs'
output_file = os.path.join(output_folder, 'output_data_training.csv')

reference_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Reference'
reference_file = os.path.join(reference_folder, 'category_reference.csv')

setup_engine(output_file, reference_file)