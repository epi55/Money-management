import os
import pandas as pd

# ENGINE
def runEngine():
    statementFolder = r"Money management\Statements"
    outputFolder = r"Money management\Outputs"

    allData = pd.DataFrame(columns=["Card", "Date of purchase", "Vendor", "Debit amount", "Credit amount" "Type of purchase", "Share"])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        data = extractEngine(filename, documentPath)
        '''allData = pd.concat([allData, pd.DataFrame({
            "Card": [pCard],
            "Date of purchase": [pDate],
            "Vendor": [pVendor],
            "Debit amount": [pDebit],
            "Credit amount": [pCredit],
            "Type of purchase": [pType],
            "Share": [pShare]})], ignore_index=True)'''

def extractEngine(filename, documentPath):
    csvData = ''

    if filename.startswith(("cibc")):
        # Column names NOT PROVIDED; added
        df = pd.read_csv(documentPath, header=None, names=['date', 'vendor', 'debit', 'credit', 'cc number'])
        pCard = filename
        pDate = df['date']
        pVendor = df['vendor']
        pDebit = df['debit']
        pCredit = df['credit']
        pType = []
        pShare = []

        df.drop(columns=['cc number'], inplace=True)

        print(df.to_string())

    if filename.startswith(("rbc")):
        # Column names PROVIDED; removed then added
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['card', 'account type', 'date', 'b1', 'vendor', 'b2', 'debit', 'b3', 'b4'])
        pCard = filename
        pDate = df['date']
        pVendor = df['vendor']
        pDebit = df['debit']
        #pCredit = df['credit']
        pType = []
        pShare = []
        
        df.drop(columns=['card', "account type", "b1", "b2", "b3", "b4"], inplace=True)
        df['credit'] = df['debit'].apply(migrateCredits)

        print(df.to_string())

        ## TODO remove positive numbers from credit column after migrateCredits, then apply absolute value to the negative numbers
        
    return csvData

def migrateCredits(amt):
    return amt if amt > 0 else None

# RUN
runEngine()
