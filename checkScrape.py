import numpy as np
import pandas as pd
# NOTE: allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])

def extractEngine(filename, filenameData, documentPath):
    if filenameData[0][1] == 'rbc':
        # COL headers provided in CSV
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['date1', 'vendor', 'debit', 'credit', 'drop1', 'drop2'])
        df.drop(columns=['drop1', 'drop2'], inplace=True)
    
    elif filenameData[0][1] == 'eq':
        # COL headers provided in CSV
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['date1', 'vendor', 'debit', 'drop1'])
        df.drop(columns=['drop1'], inplace=True)

    elif filenameData[0][1] == 'tangerine':
        # COL headers provided in CSV
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['date1', 'drop1', 'vendor', 'drop2', 'debit'])
        df.drop(columns=['drop1', 'drop2'], inplace=True)

    else:
        print("Error: \"{}\" is not from a recognized bank (i.e. RBC, EQ, or Tangerine) and will not be processed.".format(filename))
    
    cleanDataTypes(df, filenameData)
    cleanDates(df, filenameData)
    cleanStructure(df, filenameData)

    return df
    
def cleanDataTypes(df, filenameData):
    df['vendor'] = df['vendor'].astype('string')

    cleanAmounts(df, filenameData)

def cleanAmounts(df, filenameData):
    for index, row in df.iterrows():
        if row['debit'] is not None and row['debit'] != '':
            if type(row['debit']) == float:
                amount = row['debit']
            elif type(row['debit']) == str:
                amount = float(row['debit'].replace('$', '').replace(',', ''))
            df.at[index, 'debit'] = amount
        
        if filenameData[0][1] == 'rbc':
            if row['credit'] is not None and row['credit'] != '':
                if type(row['credit']) == float:
                    amount = row['credit']
                elif type(row['credit']) == str:
                    amount = float(row['credit'].replace('$', '').replace(',', ''))
                df.at[index, 'credit'] = amount

    # 'credit' is created from 'debit' if values are greater than 0
    # 'debit' values are made positive
    # 'debit' value is replaced by 'nan' if duplicated in the 'credit' column
    if filenameData[0][1] == 'eq' or filenameData[0][1] == 'tangerine':
        df['credit'] = df['debit'].apply(migrateCredits)
    
    df['debit'] = df['debit'].apply(abs)
    for index, row in df.iterrows():
        if row['debit'] == row['credit']:
            df.at[index, 'debit'] = float('nan')

def migrateCredits(credit):
    return credit if credit > 0 else None

def cleanDates(df, filenameData):
    # RBC / DD-Mon-YY = %d-%b-%y
    if filenameData[0][1] == 'rbc':
        for index, row in df.iterrows():
            date = pd.to_datetime(row['date1'], format='%d-%b-%y', errors='coerce')
            if not pd.isna(date):
                df.at[index, 'date1'] = date.strftime('%Y-%m-%d')

    # EQ / DD Mon YYYY = %d %b %Y
    if filenameData[0][1] == 'eq':
        for index, row in df.iterrows():
            date = pd.to_datetime(row['date1'], format='%d %b %Y', errors='coerce')
            if not pd.isna(date):
                df.at[index, 'date1'] = date.strftime('%Y-%m-%d')

    # TANGERINE / MM/DD/YYYY = %m/%d/%Y - NOTE: day of the month is not zero padded
    if filenameData[0][1] == 'tangerine':
        for index, row in df.iterrows():
            date = pd.to_datetime(row['date1'], format='%m/%d/%Y', errors='coerce')
            if not pd.isna(date):
                df.at[index, 'date1'] = date.strftime('%Y-%m-%d')
    
    addNewDateColumn(df)

def addNewDateColumn(df):
    df['date2'] = df['date1']
    for index, row in df.iterrows():
        date = pd.to_datetime(row['date2'], format='%Y-%m-%d', errors='coerce')
        if not pd.isna(date):
            df.at[index, 'date2'] = date.strftime('%B %d, %Y')

def cleanStructure(df, filenameData):
    df['person'] = filenameData[0][0]
    df['bank'] = filenameData[0][1]
    df['account'] = filenameData[0][2]
    
    # Unique for RBC; bank doesn't provide an date-expanded CSV / requires website copy+paste
    # NOTE: MAY NOT BE NEEDED FOR OTHER RBC CSV!!! WAS FOR DATE-EXPANDED CSVs, NOT SHORT 
    if filenameData[0][1] == 'rbc':
        dropEmptyRows(df)

def dropEmptyRows(df):
    df['vendorShifted'] = df['vendor'].shift(-1).fillna('')
    for index, row in df.iterrows():
        if index < len(df) - 1 and pd.isna(df.at[index + 1, 'date1']):
            vendorDesc = df.at[index, 'vendor'] + ' ' + df.at[index, 'vendorShifted']
            df.at[index, 'vendor'] = vendorDesc
    df.dropna(subset=['date1'], inplace=True)
    df.drop(columns=['vendorShifted'], inplace=True)