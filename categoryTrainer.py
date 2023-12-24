# IMPORTS
import pandas as pd
import numpy as np
import pathlib
import re
import os

# ENGINE
def setup_engine(output_file, reference_file):

    df_output_file = pd.read_csv(output_file, skiprows=1, header=None, usecols=[0,1,2,3,4,5,6,7,8,9], names=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])
    df_reference_file = pd.read_csv(reference_file)

    for index, row in df_output_file.iterrows():
        if pd.isna(df_output_file.at[index, 'categoryAuto']) == True:
            continue
        else:
            vendor_preclean = df_output_file.at[index, 'vendor']
            # NOTE: regex below removes extra spaces in string (before, between, after)
            vendor_postclean = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', vendor_preclean)

            ## IF CATEGORY DOES NOT EXIST, add_cateogry() + add_vendor()
            ## IF CATEGORY EXISTS BUT VENDOR DOES NOT, add_vendor()
            ## IF CATEGORY EXISTS BUT IS IDENTIFIED AS UNIQUE (i.e. accompanied with *), apply primary category but prompt input() for secondary category
            df_output_file.at[index, 'categoryAuto'] = lookup_vendor(vendor_postclean, reference_folder)

    # NOTE / TODO: NEED TO BE ADJUSTED
    if df_reference_file.empty:
        df_reference_file.loc[0] = np.nan

    if df_reference_file.isin([vendor_postclean]).any().any():
        return list(df_reference_file.columns[df_reference_file.isin([vendor_postclean]).any()])
    else:
        existing_categories = list(df_reference_file.columns)
        category_choice = input("{} not found in Look Up Tables.\n\nThe available categories are: {}.\n\nWould you like to (1) create a new category or (2) add to an existing category? ".format(vendor_postclean, existing_categories))
        new_category_name = ''

        if category_choice == '1':
            while True:
                new_category_name = input("What is the new category (or type 'back' or 'quit')? ")
                if new_category_name.lower == ('back') or new_category_name.lower == ('quit'):
                    break
                elif new_category_name in existing_categories:
                    print("Cateogry already exists. Please enter a new category name. ")
                else:
                    confirm_category_name = input("Please enter the category name again to confirm: ")
                    if confirm_category_name == new_category_name:
                        break
                    else:
                        print("Category names do not match. Please try again. ")

            # TODO BUILD OUT
            if new_category_name == ('back') or new_category_name == ('quit'):
                pass
            else:
                df_reference_file = df_reference_file.assign(**{new_category_name: vendor_postclean})
                # df_reference_file.to_csv(reference_file, index=False)
                print("New category added: \"{}\". \"{}\" assigned to category.".format(new_category_name, vendor_postclean))
         
        if category_choice == '2':
            while True:
                existing_category_name = input("What category should vendor be added to (or type 'back' or 'quit')? ")
                if existing_category_name.lower == ('back') or existing_category_name.lower == ('quit'):
                    break
                elif existing_category_name in existing_categories:
                    break
                else:
                    print("Invalid input. Please enter an existing category name. ")
            
            # TODO BUILD OUT
            if existing_category_name == ('back') or existing_category_name == ('quit'):
                pass
            else:
                mask = df_reference_file[existing_category_name].isna()
                df_reference_file.loc[mask.idxmax(), existing_category_name] = vendor_postclean
                #df_reference_file.loc[df_reference_file[existing_category_name].first_valid_index(), existing_category_name] = vendor_postclean
                #df_reference_file.at[(len(df_reference_file[existing_category_name]) + 1), existing_category_name] = vendor_postclean
                # df_reference_file.to_csv(reference_file, index=False)

            print("Existing category amended: \"{}\". \"{}\" assigned to category.".format(existing_category_name, vendor_postclean))

        df_reference_file.to_csv(reference_file, index=False)

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