# IMPORTS
import os
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ENGINES
def runEngine():
    statementFolder = r"Money management\Statements"
    outputFolder = r"Money management\Outputs"

    allData = pd.DataFrame(columns=['date', 'vendor', 'debit', 'credit', 'bank', 'card', 'category'])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        if os.path.splitext(documentPath)[1] == '.csv':
            data = extractEngine(filename, documentPath)
            allData = pd.concat([allData, data], ignore_index=True)
        else:
            print("Error: \"{}\" is not a CSV file and will be skipped.".format(filename))

    categorizerEngine(allData)
    outputEngine(allData, outputFolder)

def extractEngine(filename, documentPath):
    
    def migrateCredits(credit):
        return credit if credit > 0 else None

    def cleanDates(df):
        for index, row in df.iterrows():
            date = pd.to_datetime(row['date'], format='%m/%d/%y', errors='coerce')
            if not pd.isna(date):
                df.at[index, 'date'] = date.strftime('%Y-%m-%d')

    def filenameToCols(filename):
        drop1List = filename.split(' ')
        df['bank'] = drop1List[0]
        df['drop1'] = drop1List[1] + ' ' + drop1List[2]

    # NOTE
    # Code unique to CIBC CSV files
    # Adjustments made to standardize data structure for cf.concat
    if filename.startswith(("cibc")):
        # COL headers NOT provided in CSV 
        df = pd.read_csv(documentPath, header=None, names=['date', 'vendor', 'debit', 'credit', 'cc number'])
        df.drop(columns=['cc number'], inplace=True)

        filenameToCols(filename)
        cleanDates(df)
        return df

    # NOTE
    # Code unique to RBC CSV files
    # Adjustments made to standardize data structure for cf.concat
    elif filename.startswith(("rbc")):
        # COL headers provided in CSV
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['drop1', 'drop2', 'date', 'drop3', 'vendor', 'drop4', 'debit', 'drop5', 'drop6'])
        df.drop(columns=['drop1', "drop2", "drop3", "drop4", "drop5", "drop6"], inplace=True)
        df['credit'] = df['debit'].apply(migrateCredits)
        df['debit'] = df['debit'].apply(abs)
        for index, row in df.iterrows():
            if row['debit'] == row['credit']:
                df.at[index, 'debit'] = float('nan')

        filenameToCols(filename)
        cleanDates(df)
        return df
    
    else:
        print("##########\n# ERROR\n# \"{}\" is not a recognized bank.\n# Check filename or add additional code to parse file.\n##########".format(filename))

def categorizerEngine(df):
    
    def preprocess(vendorDesc):
        vendorDesc = vendorDesc.lower()
        vendorDesc = re.sub(r'[^\w\s]', '', vendorDesc)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        tokens = nltk.word_tokenize(vendorDesc)
        tokens = [token for token in tokens if token not in stop_words]
        stemmer = nltk.stem.PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
        
        return ' '.join(tokens)

    df['vendor'] = df['vendor'].apply(preprocess)

    # Extract features from the preprocessed vendorDesc data using bag-of-words model
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['vendor'])

    # Train a Naive Bayes classifier on the extracted features
    y = df['category']
    clf = MultinomialNB()
    clf.fit(X, y)

    # Predict categories for new transactions
    new_transactions = ['AMAZON.COM*ajlja09ja', 'Shell Oil 4106541031']
    new_transactions_preprocessed = [preprocess(vendorDesc) for vendorDesc in new_transactions]
    X_new = vectorizer.transform(new_transactions_preprocessed)
    y_new = clf.predict(X_new)

    # Print the predicted categories for new transactions
    print(y_new)

def outputEngine(allData, outputFolder):
    outputPath = os.path.join(outputFolder, "output_data.xlsx")
    allData.to_excel(outputPath, sheet_name="Statement data", index=False)
    print("Data saved to:", outputPath)

# RUN
runEngine()
