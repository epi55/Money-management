# IMPORTS
import os
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from openpyxl.workbook import Workbook
import checkScrape
import creditScrape
import pathlib
import datetime

# ENGINES
def runEngine():
    statementFolder = pathlib.Path('Money management') / 'Scraper' / 'Statements'
    outputFolder = pathlib.Path('Money management') / 'Scraper' / 'Outputs'
    
    allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'category1', 'category2', 'person'])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        filenameData = re.findall(r'([^-]+) - ([^-]+) - ([^-]+) - ([^-]+)(- [^-]+)?', filename)
        processedToken = "- prc YYYY-MM-DD"

        if filename[-20:-4].startswith('- prc'):
            continue
        else:
            if os.path.splitext(documentPath)[1] == '.csv':
                if filenameData[0][2] == 'checking':
                    data = checkScrape.extractEngine(filename, filenameData, documentPath)
                    allData = pd.concat([allData, data], ignore_index=True)
                elif 'amex' or 'mastercard' or 'visa' in filenameData[0][2]:
                    data = creditScrape.extractEngine(filename, filenameData, documentPath)
                    allData = pd.concat([allData, data], ignore_index=True)
                else:
                    print("Error: \"{}\" is not a recognized account type (i.e., checking, amex, mastercard, or visa).".format(filename))
                
                nameChange(documentPath)
            
            else:
                print("Error: \"{}\" is not a CSV file and will not be processed.".format(filename))

    outputChoice = input("## '1' for CSV ## '2' for EXCEL: ")
    outputEngine(allData, outputFolder, outputChoice)

def nameChange(documentPath):
    currentDate = datetime.datetime.now()
    dateStr = currentDate.strftime("%Y-%m-%d")
    
    oldFilename = documentPath
    filenameWithoutExtension = os.path.splitext(oldFilename)[0]
    newFilename = "{} - prc {}.csv".format(filenameWithoutExtension, dateStr)
    os.rename(oldFilename, newFilename)

def outputEngine(allData, outputFolder, outputChoice):
    if outputChoice == '1':
        outputPath = os.path.join(outputFolder, 'output_data.csv')

        if os.path.exists(outputPath):
            dfExisting = pd.read_csv(outputPath)
            df = pd.concat([allData, dfExisting])
            df = df.drop_duplicates(subset=['date1', 'vendor', 'debit', 'credit', 'bank', 'account', 'person'])
            df.csv(outputPath, index=False)
        else:
            allData.to_csv(outputPath, index=False)

        print("Data saved to:", outputPath)

    if outputChoice == '2':
        outputPath = os.path.join(outputFolder, 'output_data.xlsx')

        if os.path.exists(outputPath):
            dfExisting = pd.read_excel(outputPath)
            df = pd.concat([allData, dfExisting])
            df = df.drop_duplicates(subset=['date1', 'vendor', 'debit', 'credit', 'bank', 'account', 'person'])
            df.to_excel(outputPath, index=False)
        else:
            allData.to_excel(outputPath, index=False)

        print("Data saved to: {}".format(outputPath))

# RUN
runEngine()
