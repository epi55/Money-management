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
import pathLib

# ENGINES
def runEngine():
    #statementFolder = r"Money management\Scraper\Statements"
    #outputFolder = r"Money management\Scraper\Outputs"

    statementFolder = pathlib.Path('Money management') / 'Scraper' / 'Statements'
    outputFolder = pathlib.Path('Money management') / 'Scraper' / 'Outputs'
    
    allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'category1', 'category2', 'person'])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        filenameData = re.findall(r"([^-]+) - ([^-]+) - ([^-]+) - ([^.]+)", filename)

        if os.path.splitext(documentPath)[1] == '.csv':
            if filenameData[0][2] == 'checking':
                data = checkScrape.extractEngine(filename, filenameData, documentPath)
                allData = pd.concat([allData, data], ignore_index=True)
            elif 'amex' or 'mastercard' or 'visa' in filenameData[0][2]: 
                data = creditScrape.extractEngine(filename, filenameData, documentPath)
                allData = pd.concat([allData, data], ignore_index=True)
            else:
                print("Error: \"{}\" is not a recognized account type (i.e., checking, amex, mastercard, or visa).".format(filename))
        
        else:
            print("Error: \"{}\" is not a CSV file and will not be processed.".format(filename))

    outputChoice = input("## '1' for CSV ## '2' for EXCEL: ")
    outputEngine(allData, outputFolder, outputChoice)

def outputEngine(allData, outputFolder, outputChoice):
    if outputChoice == '1':
        outputPath = os.path.join(outputFolder, "output_data.csv")
        allData.to_csv(outputPath, index=False)
        print("Data saved to:", outputPath)

    if outputChoice == '2':
        outputPath = os.path.join(outputFolder, "output_data.xlsx")
        allData.to_excel(outputPath, index=False)
        print("Data saved to:", outputPath)

# RUN
runEngine()
