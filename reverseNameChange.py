# IMPORTS
import os
import pathlib

# ENGINES
def removeFilenameStr(folderPath, strToRemove):
    for filename in os.listdir(folderPath):
        if filename.endswith(strToRemove):
            old_path = os.path.join(folderPath, filename)
            new_path = os.path.join(folderPath, filename[:-len(strToRemove)] + '.csv')
            os.rename(old_path, new_path)

# RUN
folderPath = pathlib.Path('Money management') / 'Scraper' / 'Statements'
strToRemove = '  - prc 2023-11-10.csv' # NOTE: Pay attention to extra spaces and file extensions.
removeFilenameStr(folderPath, strToRemove)