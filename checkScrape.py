import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook
# NOTE: allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'category1', 'category2', 'person'])

def extractEngine(filename, filenameData, documentPath):
    if filenameData[0][1] == 'rbc':
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['date1', 'vendor', 'debit', 'credit', 'balance', 'drop1'])
    else:
        print("Error: \"{}\" is not from a recognized bank (i.e. RBC) and will not be processed.".format(filename))
    
    cleanDataTypes(df)
    cleanDates(df)
    cleanStructure(df, filenameData)

    return df
    
def cleanDataTypes(df):
    df['vendor'] = df['vendor'].astype('string')

    cleanAmounts(df)

def cleanAmounts(df):
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

def cleanDates(df):
    for index, row in df.iterrows():
        date = pd.to_datetime(row['date1'], format='%d-%b-%y', errors='coerce') # ORIGINAL: format='%m/%d/%y'
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
    df.drop(columns=['drop1', 'balance'], inplace=True)

    dropEmptyRows(df)

def dropEmptyRows(df):
    def concat_strings(x):
        return ' '.join(x)
    df = df.groupby(['date1', 'date2', 'debit', 'credit', 'bank', 'account', 'person'])['vendor'].agg(concat_strings).reset_index()
    # NOTE: groupby code above, I removed 'category1' and 'category2'
    df = df.dropna(subset=['date1'], inplace=True)

'''def dropEmptyRows(df):
    for index, row in df.iterrows():
        if index != 0 or index != len(df):
            if row['date1'] is None or '':
                vendorDesc = df.iloc[index-1]['vendor'] + ' ' + df.iloc[index]['vendor']
                df.iloc[index-1]['vendor'] = vendorDesc'''

'''    df['credit'] = df['debit'].apply(migrateCredits)
    df['debit'] = df['debit'].apply(abs)
    for index, row in df.iterrows():s
        if row['debit'] == row['credit']:
            df.at[index, 'debit'] = float('nan')'''
