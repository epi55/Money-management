# Money-Management
## Purpose:
Script parses credit card and checking acount statements from select banks.
* Extracts data from CSV files, cleans and processes data into a desired format with Pandas, and exports data into an Excel or CSV file.

## CURRENT
* Focus: Script needs to update a persistent database instead of creating a new one on each run. Will need to add new entries into the database while ignoring duplicates.

## FUTURE
* Create a lookup dictionary to populate recurring cost categories (e.g. groceries).
* Design and develop automated biweekly Excel spreadsheet; instead of manual entry every two weeks, relevant data will be extracted from inputs (e.g. pay stub, credit and checking statements), processed, calculated, and presented in a dashboard similar to existing manual Excel.
* NLP for cost categories.
* Saving and investment data extraction and analysis.

## COMPLETED
* Added function to rename documents after they're processed. (2023/11/10)
* Added conditional statement to skip document if it's been processed (via token in changed name). (2023/11/10)
* Created a script (reverseNameChange.py) to support development testing; script modifies file names, if code errors occur. (2023/11/10)
