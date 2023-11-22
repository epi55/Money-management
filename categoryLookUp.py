# Future work (after lookup): MCC Merchant Category Codes needed for Mastercard, Visa, and American Express
# SEE: https://github.com/greggles/mcc-codes/blob/main/mcc_codes.csv

import pandas as pd

# load df, iterate through rows (inefficient) to find empty category columns
# prep for vendor lookup in categoryLookUp
def checkCategories(df, referenceFolder):
    for index, row in df.iterrows():
        if pd.isna(df.at[index, 'category1']): # NOTE: Can update category1, category2 names => "categoryAuto", "categoryManual"
            vendorPreClean = df.at[index, 'vendor']
            vendorPostClean = re.sub(r'[^a-zA-Z]', '', vendorPreClean)
            df.at[index, 'category1'] = vendorLookUp(vendorPostClean, referenceFolder)

def vendorLookUp(vendorPostClean, referenceFolder):
    referencePath = os.path.join(referenceFolder, 'categoryLookUp.csv')
    dfLookUp = pd.read_csv(referencePath)
    if dfLookUp.isin([vendorPostClean]).any().any():
        return list(df.columns[df.isin([vendorPostClean]).any()])
    else:
        existingCategories = list(dfLookUp.columns)
        categoryChoice = input("{} not found in Look Up Tables. The available categories are: {}. Would you like to (1) create a new category or (2) add to an existing category?".format(vendorPostClean, existingCategories))
        if categoryChoice == '1':
            # CREATE CATEGORY
            newCategoryName = input("What is the new category?")
            dfLookUp = dfLookUp.assign(newCategoryName=[vendorPostClean])
            df.to_csv(referencePath, index=False)
            print("New category added: \"{}\". \"{}\" added to category as a vendor.".format(newCategoryName, vendorPostClean))
        if categoryChoice == '2':
            # ADD TO CATEGORY
            existingCategoryName = input("What category do you want to add the vendor to?")
            print("Existing category amended: \"{}\". \"{}\" added to category as a vendor.".format(newCategoryName, vendorPostClean))


# NOTE: Not sure how to handle the lookup. Dataframe might not be great, but could it be lists instead? Am I making it overly complicated? I want to use a csv file though.

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