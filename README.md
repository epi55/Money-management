# Money-Management
## Purpose:
* Script to parse financial statements from banking accounts and credit cards.
* Extracts data from CSV files, cleans and processes data into a desired format with Pandas, and exports data into an Excel and CSV database.

## CURRENT
* Focus: Script needs to update a persistent database instead of creating a new one on each run, adding new entries into the database while ignoring duplicates.
  * Status: Developed and debugging.
* Create a lookup dictionary to populate recurring cost categories (e.g. groceries).
  * Status: Developed and testing core functionality.

## FUTURE
* Enhancement: NLP to identify categories for transactions based on vendor description.
* Enhancement: Merchant Category Codes (MCC) to identify categories for transactions.
* Enhancement: Data analysis and visualization. For example, sums of categories (and sub-categories) in a Sankey diagram to represent how the money was used and where it went.
* New module: Implement an automated biweekly Excel spreadsheet. Instead of manual entry every two weeks, relevant data will be extracted from inputs (e.g. pay stub, credit and checking statements), processed, calculated, and presented in a dashboard similar to existing manual Excel.
* New module: Saving and investment data extraction and analysis.

## COMPLETED
* Added function to rename documents after they're processed. (2023/11/10)
* Added conditional statement to skip document if it's been processed (via token in changed name). (2023/11/10)
* Created a script (reverseNameChange.py) to support development testing; script modifies file names, if code errors occur. (2023/11/10)
* Revised script to check for an existing Excel file and add non-duplicates to its data, preserving unique data added post-scraping (e.g. user input like categories). (2023/11/19)
* Revised output function to include both Excel and Excel + CSV outputs. (2023/11/20)

## KNOWN ISSUES
* Certain banks don't provide statement downloads (or are poor). Manual processing of statements required. Some code features might reduce manual processing, including: (1) detecting and replacing certain characters in strings (e.g. '$') that cause errors; (2) dynamically detecting date patterns; and (3) dynamically detecting debit and credit values in merged columns (e.g. based on sampling of known vendor behavior).
