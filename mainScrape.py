# IMPORTS
import os
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
import checkScrape
import creditScrape
import pathlib
import datetime

# ENGINES
def runEngine():
    statementFolder = pathlib.Path('Money management') / 'Scraper' / 'Statements'
    outputFolder = pathlib.Path('Money management') / 'Scraper' / 'Outputs'
    referenceFolder = pathlib.Path('Money management') / 'Scraper' / 'Reference'
    
    allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])

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
                
                # nameChange(documentPath) ## REMOVED FOR TESTING
            
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

def outputEngine(dfScraped, outputFolder, outputChoice):
    outputPath = os.path.join(outputFolder, 'output_data.xlsx')

    if os.path.exists(outputPath):
        with pd.ExcelWriter(outputPath, mode='a', if_sheet_exists='overlay') as writer:
            dfExcel = pd.read_excel(outputPath, sheet_name='Sheet1')
            dfCombined = pd.concat([dfExcel, dfScraped])
            dfUnique = dfCombined.drop_duplicates(subset=['date1', 'vendor', 'debit', 'credit', 'bank', 'account', 'person'], keep='first')

            categoryChoice = None
            while categoryChoice not in ['Y', 'N']:
                categoryChoice = input("Do you want to automatically categorize new entries? Y/N")
            
            if categoryChoice == 'Y':
                dfUnique = categoryLookUp.checkEngine(dfUnique, referenceFolder)

            dfUnique.to_excel(writer, sheet_name='Sheet1', index=False)
            print("(Scraped and extract) Data saved as Excel to:", outputPath)
            if outputChoice == '1':
                outputPath = os.path.join(outputFolder, 'output_data.csv')
                dfUnique.to_csv(outputPath, index=False)
                print("(Scraped and extract) Data saved as CSV to:", outputPath)

    else:
        categoryChoice = None
        while categoryChoice not in ['Y', 'N']:
            categoryChoice = input("Do you want to automatically categorize new entries? Y/N")

        if categoryChoice == 'Y':
            dfScraped = categoryLookUp.checkEngine(dfScraped, referenceFolder)
        
        dfScraped.to_excel(outputPath, index=False)
        print("(Scraped only) Data saved as Excel to:", outputPath)
        if outputChoice == '1':
            outputPath = os.path.join(outputFolder, 'output_data.csv')
            dfScraped.to_csv(outputPath, index=False)
            print("(Scraped only) Data saved as CSV to:", outputPath)

# RUN
runEngine()