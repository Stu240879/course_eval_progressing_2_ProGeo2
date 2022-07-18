
import pandas as pd

def sampleData():
    import os
    dirname = os.path.dirname(__file__)
    fp = os.path.join(dirname, 'data\survey.xlsx')
    return fp


def loadData(file = "", nrows=0):
    data = pd.read_excel(file, sheet_name="Eval")
    colnames = data.iloc[0,:]
    # print(colnames)
    quest = data.iloc[1,:]
    data = data[2::]
    data.columns = colnames
    data.reset_index(inplace=True, drop=True)
    # print(data)
    # data.index = data.iloc[:,0].astype(int)
    
    # returns all except header
    return data

def getQuestions(file="",nrows=0):
    data = pd.read_excel(file, sheet_name="Fragen")
    return data





if __name__ == "__main__":

    foo = sampleData()
    bar = loadData(file=foo)
    baz = getQuestions(file=foo)
    print(baz)
