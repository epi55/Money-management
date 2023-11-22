import numpy as np
import pandas as pd
# NOTE: allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])

def extractEngine(filename, filenameData, documentPath):
    if filenameData[0][1] == 'cibc':
        # COL headers NOT provided in CSV 
        df = pd.read_csv(documentPath, header=None, names=['date1', 'vendor', 'debit', 'credit', 'drop1'])
        df.drop(columns=['drop1'], inplace=True)
        
    elif filenameData[0][1] == 'rbc':
        # COL headers provided in CSV
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['drop1', 'drop2', 'date1', 'drop3', 'vendor', 'drop4', 'debit', 'drop5', 'drop6'])
        df.drop(columns=['drop1', 'drop2', 'drop3', 'drop4', 'drop5', 'drop6'], inplace=True)
        
    elif filenameData[0][1] == 'hsbc':
        # COL headers NOT provided in CSV
        df = pd.read_csv(documentPath, header=None, names=['drop1', 'date1', 'vendor', 'debit'])
        df.drop(columns=['drop1'], inplace=True)
   
    else:
        print("##########\n# ERROR\n# \"{}\" is not a recognized bank.\n# Check filename or add additional code to parse file.\n##########".format(filename))
    
    cleanDataTypes(df, filenameData)
    cleanDates(df)
    cleanStructure(df, filenameData)

    return df
    
def cleanDataTypes(df, filenameData):
    df['vendor'] = df['vendor'].astype('string')

    if filenameData[0][1] == 'rbc' or filenameData[0][1] == 'hsbc':
        cleanAmounts(df, filenameData)

def cleanAmounts(df, filenameData):
    # NOTE: Raw data uses 1 column for debit and credit
    # 'credit' is created from 'debit' if values are greater than 0
    # 'debit' values are made positive
    # 'debit' value is replaced by 'nan' if duplicated in the 'credit' column
    df['credit'] = df['debit'].apply(migrateCredits)
    df['debit'] = df['debit'].apply(abs)
    for index, row in df.iterrows():
        if row['debit'] == row['credit']:
            df.at[index, 'debit'] = float('nan')    

    for index, row in df.iterrows():
        if row['debit'] is not None and row['debit'] != '':
            if type(row['debit']) == float:
                amount = row['debit']
            elif type(row['debit']) == str:
                amount = float(row['debit'].replace('$', '').replace(',', ''))
            df.at[index, 'debit'] = amount

        if row['credit'] is not None and row['credit'] != '':
            if type(row['credit']) == float:
                amount = row['credit']
            elif type(row['credit']) == str:
                amount = float(row['credit'].replace('$', '').replace(',', ''))
            df.at[index, 'credit'] = amount

def migrateCredits(credit):
    credit = pd.to_numeric(credit)
    return credit if credit > 0 else None

def cleanDates(df):
    for index, row in df.iterrows():
        date = pd.to_datetime(row['date1'], format='%d-%b-%y', errors='coerce')
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