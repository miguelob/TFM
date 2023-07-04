import pandas as pd
import tkinter as tk


def returnNames():
    # return the first column
    return df.iloc[:,0].tolist()
# Replace 'path/to/file.xlsx' with the actual path to your Excel file

def returnValues(name):
    #returns all the rows with the name mathing the first column
    return df.loc[df['Dapp name'] == name].values.tolist()[0][1:]



df = pd.read_excel("./database.xlsx")



#remove NaN
df = df.dropna()
# remove duplicates
df = df.drop_duplicates()
# remove rows with no data
df = df.dropna(how='all')



