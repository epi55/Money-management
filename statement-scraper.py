import os
import pandas as pd

# ENGINE
def runEngine():
    statementFolder = r"Money management\Statements"
    outputFolder = r"Money management\Outputs"

    allData = pd.DataFrame(columns=["Card", "Date of purchase", "Vendor", "Amount of purchase", "Type of purchase", "Share"])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        data = extractEngine(filename, documentPath)
        '''allData = pd.concat([allData, pd.DataFrame({
            "Card": [pCard],
            "Date of purchase": [pDate],
            "Vendor": [pVendor],
            "Amount of purchase": [pAmount],
            "Type of purchase": [pType],
            "Share": [pShare]})], ignore_index=True)'''

def extractEngine(filename, documentPath):
    csvData = ''

    if filename.startswith(("cibc")):
        # Column names NOT PROVIDED; added
        df = pd.read_csv(documentPath, header=None, names=['date', 'vendor', 'amount', 'credit', 'cc number'])
        pCard = filename
        pDate = df['date']
        pVendor = df['vendor']
        pAmount = df['amount']
        pType = []
        pShare = []

        #print(df.to_string())
        #print("#####\n# Filename: {}\n# pDate: {}\n# pVendor: {}\n# pAmount: {}\n#####".format(filename, pDate[0], pVendor[0], pAmount[0]))

    if filename.startswith(("rbc")):
        # Column names PROVIDED; removed then added
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['card', 'account type', 'date', 'b1', 'vendor', 'b2', 'amount', 'b3', 'b4'])
        pCard = filename
        pDate = df['date']
        pVendor = df['vendor']
        pAmount = -(df['amount']) # RBC credits and debits are inverse
        pType = []
        pShare = []
        
        #print(df.to_string())
        #print("#####\n# Filename: {}\n# pDate: {}\n# pVendor: {}\n# pAmount: {}\n#####".format(filename, pDate[0], pVendor[0], pAmount[0]))
        
    return csvData

# RUN
runEngine()