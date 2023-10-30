import os
import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook

# ENGINE
def runEngine():
    statementFolder = r"Money management\Statements"
    outputFolder = r"Money management\Outputs"

    allData = pd.DataFrame(columns=['date', 'vendor', 'debit', 'credit', 'bank', 'card'])

    for filename in os.listdir(statementFolder):
        documentPath = os.path.join(statementFolder, filename)
        data = extractEngine(filename, documentPath)
        allData = pd.concat([allData, data], ignore_index=True)

    outputEngine(allData, outputFolder)

def extractEngine(filename, documentPath):
    if filename.startswith(("cibc")):
        # Column names NOT PROVIDED; added
        df = pd.read_csv(documentPath, header=None, names=['date', 'vendor', 'debit', 'credit', 'cc number'])

        df.drop(columns=['cc number'], inplace=True)

        # TODO Automate based on filename (need to standardize)
        cardList = filename.split(' ')
        df['bank'] = cardList[0]
        df['card'] = cardList[1] + ' ' + cardList[2]

        return df

    if filename.startswith(("rbc")):
        # Column names PROVIDED; removed then added
        df = pd.read_csv(documentPath, skiprows=1, header=None, names=['card', 'account type', 'date', 'b1', 'vendor', 'b2', 'debit', 'b3', 'b4'])
        
        # DATA STD: CREDIT + DEBIT
        df.drop(columns=['card', "account type", "b1", "b2", "b3", "b4"], inplace=True)
        df['credit'] = df['debit'].apply(migrateCredits)
        df['debit'] = df['debit'].apply(abs)
        for index, row in df.iterrows():
            if row['debit'] == row['credit']:
                df.at[index, 'debit'] = float('nan')

        # DATA STD: DATE
        #for index, row in df.iterrows():
        #    df.at[index, 'date'] = pd.to_datetime(row['date'], format='%m/%d/%Y').strftime('%Y-%m-%d')

        # TODO Automate based on filename (need to standardize)
        cardList = filename.split(' ')
        df['bank'] = cardList[0]
        df['card'] = cardList[1] + ' ' + cardList[2]

        return df

def migrateCredits(credit):
    return credit if credit > 0 else None

def categorizerEngine(df):
    
    def preprocess(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token not in stop_words]
        stemmer = nltk.stem.PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
        
        return ' '.join(tokens)

    df['vendor'] = df['vendor'].apply(preprocess)

    # Extract features from the preprocessed text data using bag-of-words model
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['Description'])

    # Train a Naive Bayes classifier on the extracted features
    y = df['Category']
    clf = MultinomialNB()
    clf.fit(X, y)

    # Predict categories for new transactions
    new_transactions = ['AMAZON.COM*ajlja09ja', 'Shell Oil 4106541031']
    new_transactions_preprocessed = [preprocess(text) for text in new_transactions]
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
