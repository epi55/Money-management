# Future work (after lookup): MCC Merchant Category Codes needed for Mastercard, Visa, and American Express
# SEE: https://github.com/greggles/mcc-codes/blob/main/mcc_codes.csv

import pandas as pd

# load df, parse through to a 
def checkCategory(df):
    vendorPreClean = ''
    vendorPostClean = re.sub(r'[^a-zA-Z]', '', vendorPreClean)

def cleanCategory():
    continue

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