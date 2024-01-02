import os
import re
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
import pathlib
import datetime
import checkScrape # custom script
import creditScrape # custom script
import categoryLookup # custom script

## future IMPORTS
# import nltk
# from nltk.corpus import stopwords

# ENGINES
def run_engine(statement_folder, output_folder, reference_folder):
    allData = pd.DataFrame(columns=['date1', 'date2', 'vendor', 'debit', 'credit', 'bank', 'account', 'categoryAuto', 'categoryManual', 'person'])

    for filename in os.listdir(statement_folder):
        documentPath = os.path.join(statement_folder, filename)
        filenameData = re.findall(r'([^-]+) - ([^-]+) - ([^-]+) - ([^-]+)(- [^-]+)?', filename)
        processedToken = '- prc YYYY-MM-DD' # Needed?

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
    outputEngine(allData, output_folder, outputChoice, reference_folder)

def nameChange(documentPath):
    currentDate = datetime.datetime.now()
    dateStr = currentDate.strftime("%Y-%m-%d")
    
    oldFilename = documentPath
    filenameWithoutExtension = os.path.splitext(oldFilename)[0]
    newFilename = "{} - prc {}.csv".format(filenameWithoutExtension, dateStr)
    os.rename(oldFilename, newFilename)

def outputEngine(dfScraped, output_folder, outputChoice, reference_folder):
    outputPath = os.path.join(output_folder, 'output_data.xlsx')

    # SCRAPED AND EXTRACT
    if os.path.exists(outputPath):
        with pd.ExcelWriter(outputPath, mode='a', if_sheet_exists='overlay') as writer:
            dfExcel = pd.read_excel(outputPath, sheet_name='Sheet1')
            dfCombined = pd.concat([dfExcel, dfScraped])
            dfUnique = dfCombined.drop_duplicates(subset=['date1', 'vendor', 'debit', 'credit', 'bank', 'account', 'person'], keep='first')

            categoryChoice = ''
            while categoryChoice.lower() not in ['y', 'n']:
                categoryChoice = input("\nDo you want to automatically categorize new entries? Y/N ")
            
            if categoryChoice.lower() == 'y':
                dfUnique = categoryLookup.lookup_engine(dfUnique, reference_folder)

            dfUnique.to_excel(writer, sheet_name='Sheet1', index=False)
            print("(Scraped and extract) Data saved as Excel to:", outputPath)
            if outputChoice == '1':
                outputPath = os.path.join(output_folder, 'output_data.csv')
                dfUnique.to_csv(outputPath, index=False)
                print("(Scraped and extract) Data saved as CSV to:", outputPath)

    # SCRAPED ONLY
    else:
        categoryChoice = ''
        while categoryChoice.lower() not in ['y', 'n']:
            categoryChoice = input("\nDo you want to automatically categorize new entries? Y/N ")

        if categoryChoice.lower() == 'y':
            dfScraped = categoryLookup.lookup_engine(dfScraped, reference_folder)
        
        dfScraped.to_excel(outputPath, index=False)
        print("(Scraped only) Data saved as Excel to:", outputPath)
        if outputChoice == '1':
            outputPath = os.path.join(output_folder, 'output_data.csv')
            dfScraped.to_csv(outputPath, index=False)
            print("(Scraped only) Data saved as CSV to:", outputPath)

# RUN
statement_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Statements'
output_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Outputs'
reference_folder = pathlib.Path('Projects') / 'Money Management' / 'Scraper' / 'Reference'

run_engine(statement_folder, output_folder, reference_folder)