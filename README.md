# Money-Management
## Purpose:
Script parses credit card and checking acount statements from select banks.
* Extracts data from CSV files, cleans and processes data into a desired format with Pandas, and exports data into an Excel or CSV file.

## CURRENT
## FUTURE
* Script needs to update a persistent database instead of creating a new one on each run. Will need to add new entries into the database while ignoring duplicates.
## COMPLETED
* Added function to rename documents after they're processed. (2023/11/10)
* Added conditional statement to skip document if it's been processed (via token in changed name). (2023/11/10)
