# IMPORTS
import pandas as pd
import numpy as np
import pathlib
import re
import os

# ENGINE
def setup_engine(output_file, reference_file):

    df_output_file = pd.read_csv(output_file, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,9], names=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])

    print(df_output_file)

    for index, row in df_output_file.iterrows():
        # NOTE: pass by empty cells
        if pd.isna(df_output_file.at[index, 'categoryAuto']) == True:
            continue
        # NOTE: if cell isn't empty, process it
        else:
            vendor_preclean = df_output_file.at[index, 'vendor']
            # NOTE: regex below removes extra spaces in string (before, between, after)
            vendor_postclean = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', vendor_preclean)

            ## IF CATEGORY EXISTS BUT VENDOR DOES NOT, add_vendor()
            ## IF CATEGORY DOES NOT EXIST, add_cateogry() + add_category()
            ## IF CATEGORY IS IDENTIFIED AS UNIQUE (i.e. accompanied with *), apply primary category but prompt input() for secondary category
            df_output_file.at[index, 'categoryAuto'] = lookup_vendor(vendor_postclean, reference_folder)

def add_category():
    pass

def add_vendor():
    pass

# RUN
## TODO: Can these be done together? output_folder and output_file, etc.
statement_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Statements'

output_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Outputs'
output_file = os.path.join(output_folder, 'output_data_training.csv')

reference_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Reference'
reference_file = os.path.join(reference_folder, 'category_reference.csv')

setup_engine(output_file, reference_file)