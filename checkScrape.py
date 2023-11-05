import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook

def runEngine():
    statementFolder = r"Money management\Scraper\Statements"
    outputFolder = r"Money management\Scraper\Outputs"

    allData = pd.DataFrame(columns=['date', 'vendor', 'debit', 'credit', 'bank', 'card', 'category'])

    for filename in os.listdir(statementFolder):
        filenameData = re.findall(r"([^-]+) - ([^-]+) - ([^-]+) - ([^.]+)", filename)
        documentPath = os.path.join(statementFolder, filename)
        if os.path.splitext(documentPath)[1] == '.csv':
            data = extractEngine(filename, documentPath)
            allData = pd.concat([allData, data], ignore_index=True)
        else:
            print("Error: \"{}\" is not a CSV file and will be skipped.".format(filename))

    outputEngine(allData, outputFolder, outputChoice)