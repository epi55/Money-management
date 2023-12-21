import pandas as pd
import numpy as np
import re
import os

# TODO: iterrows is inefficient; how can performance be improved?
# NOTE:
# function iterates through df, identifies whether 'categoryAuto' column is empty, if empty then it cleans vendor description,
# sends vendor description into another function to identify whether it can be automatically categorized, and then
# returns the updated dataframe back to mainScrape.py.
def lookup_engine(df, reference_folder):
    for index, row in df.iterrows():
        if pd.isna(df.at[index, 'categoryAuto']):
            vendor_preclean = df.at[index, 'vendor']
            # NOTE: regex below removes extra spaces in string (before, between, after)
            vendor_postclean = re.sub(r'(?<=\w) +(?=\w)|(?<=\w) +$|^ +| +(?=\w)', '', vendor_preclean)
            df.at[index, 'categoryAuto'] = lookup_vendor(vendor_postclean, reference_folder)
    
    # NOTE: returns modified df back to mainScrape.py
    return df

def lookup_vendor(vendor_postclean, reference_folder):
    reference_file = os.path.join(reference_folder, 'category_reference.csv')
    df_lookup = pd.read_csv(reference_file)

    # TODO: CURRENT ISSUE !!!
    # NOTE: unless script is ran as an original init, this test will never run
    if df_lookup.empty:
        df_lookup.loc[0] = np.nan

    if df_lookup.isin([vendor_postclean]).any().any():
        return list(df_lookup.columns[df_lookup.isin([vendor_postclean]).any()])
    else:
        existing_categories = list(df_lookup.columns)
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
                df_lookup = df_lookup.assign(**{new_category_name: vendor_postclean})
                # df_lookup.to_csv(reference_file, index=False)
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
                mask = df_lookup[existing_category_name].isna()
                df_lookup.loc[mask.idxmax(), existing_category_name] = vendor_postclean
                #df_lookup.loc[df_lookup[existing_category_name].first_valid_index(), existing_category_name] = vendor_postclean
                #df_lookup.at[(len(df_lookup[existing_category_name]) + 1), existing_category_name] = vendor_postclean
                # df_lookup.to_csv(reference_file, index=False)

            print("Existing category amended: \"{}\". \"{}\" assigned to category.".format(existing_category_name, vendor_postclean))

        df_lookup.to_csv(reference_file, index=False)

# Check category column
#
# (1a)> if category is empty:
#     > Assign a variable to the value of Vendor column
#     > Clean and process variable (remove numbers, non alpha-numeric characters, etc.)
#
# (2) > Lookup variable in the Lookup CSV file
#     > Key: Value, Category: Vendor
#     
# (3a)> if variable in Value (Vendor):
#     > update Vendor column with Key
#     
# (3b)> if variable not in Value (Vendor):
#     > prompt for user input to assign a category
#
# (4a)> if user input in Key (Category):
#     > add variable as a Value to Key
#
# (4b)> if user input not in Key (Category):
#     > print("Not a valid Key. Do you want to add this category?")
#
# (5a)> if user wants category added:
#     > add user input as Key (Category)
#
# (5b)> if user does not want category added:
#     > update Vendor column with "uncategorized"
#
# (1b)> if category is not empty:
#     > skip