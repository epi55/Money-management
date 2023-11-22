# Future work (after lookup): MCC Merchant Category Codes needed for Mastercard, Visa, and American Express
# SEE: https://github.com/greggles/mcc-codes/blob/main/mcc_codes.csv

import pandas as pd

# NOTE / TODO : iterrows is inefficient; how can performance be improved?
def checkEngine(df, referenceFolder):
    for index, row in df.iterrows():
        if pd.isna(df.at[index, 'categoryAuto']):
            vendorPreClean = df.at[index, 'vendor']
            vendorPostClean = re.sub(r'[^a-zA-Z]', '', vendorPreClean)
            df.at[index, 'categoryAuto'] = vendorLookUp(vendorPostClean, referenceFolder)

def vendorLookUp(vendorPostClean, referenceFolder):
    referencePath = os.path.join(referenceFolder, 'categoryLookUp.csv')
    dfLookUp = pd.read_csv(referencePath)
    
    # NOTE / TODO : This may return multiple categories; how do we handle this?
    if dfLookUp.isin([vendorPostClean]).any().any():
        return list(df.columns[df.isin([vendorPostClean]).any()])
    else:
        existingCategories = list(dfLookUp.columns)
        categoryChoice = input("{} not found in Look Up Tables. The available categories are: {}. Would you like to (1) create a new category or (2) add to an existing category?".format(vendorPostClean, existingCategories))
        
        if categoryChoice == '1':
            while True:
                newCategoryName = input("What is the new category?")
                if newCategoryName in existingCategories:
                    print("Cateogry already exists. Please enter a new category name.")
                else:
                    confirmCategoryName = input("Please enter the category name again to confirm: ")
                    if confirmCategoryName == newCategoryName:
                        break
                    else:
                        print("Category names do not match. Please try again.")

            dfLookUp = dfLookUp.assign(newCategoryName=[vendorPostClean])
            df.to_csv(referencePath, index=False)
            print("New category added: \"{}\". \"{}\" assigned to category.".format(newCategoryName, vendorPostClean))
         
        if categoryChoice == '2':
            # ADD TO CATEGORY
            while True:
                existingCategoryName = input("What category should vendor be added to?")
                if existingCategoryName in existingCategories:
                    break
                else:
                    print("Invalid input. Please enter an existing category name.")
            
            index = dfLookUp[existingCategoryName].isnull().idxmax()
            dfLookUp.loc[index, existingCategoryName] = vendorPostClean
            print("Existing category amended: \"{}\". \"{}\" assigned to category.".format(existingCategoryName, vendorPostClean))

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