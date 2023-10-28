import os
import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook

# ENGINE
def runEngine():
    statementFolder = r"Money management\Statements"
    outputFolder = r"Money management\Outputs"

    allData = pd.DataFrame(columns=['date', 'vendor', 'debit', 'credit', 'bank', 'card'])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        data = extractEngine(filename, documentPath)
        allData = pd.concat([allData, data], ignore_index=True)

    outputEngine(allData, outputFolder)

def extractEngine(filename, documentPath):
    if filename.startswith(("cibc")):
        # Column names NOT PROVIDED; added
        df = pd.read_csv(documentPath, header=None, names=['date', 'vendor', 'debit', 'credit', 'cc number'])

        df.drop(columns=['cc number'], inplace=True)

        # TODO Automate based on filename (need to standardize)
        df['bank'] = 'CIBC'
        df['card'] = 'VISA'

        return df

    if filename.startswith(("rbc")):
        # Column names PROVIDED; removed then added
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['card', 'account type', 'date', 'b1', 'vendor', 'b2', 'debit', 'b3', 'b4'])
        
        # DATA STD: CREDIT + DEBIT
        df.drop(columns=['card', "account type", "b1", "b2", "b3", "b4"], inplace=True)
        df['credit'] = df['debit'].apply(migrateCredits)
        df['debit'] = df['debit'].apply(abs)
        for index, row in df.iterrows():
            if row['debit'] == row['credit']:
                df.at[index, 'debit'] = float('nan')

        # DATA STD: DATE
        for index, row in df.iterrows():
            df.at[index, 'date'] = pd.to_datetime(row['date'], format='%m/%d/%Y').strftime('%Y-%m-%d')

        # TODO Automate based on filename (need to standardize)
        df['bank'] = 'RBC'
        df['card'] = 'VISA'

        return df

def migrateCredits(credit):
    return credit if credit > 0 else None

def outputEngine(allData, outputFolder):
    outputPath = os.path.join(outputFolder, "output_data.xlsx")
    allData.to_excel(outputPath, sheet_name="Statement data", index=False)

    print("Data saved to:", outputPath)

# RUN
runEngine()
