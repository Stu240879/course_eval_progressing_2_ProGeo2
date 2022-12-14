
import pandas as pd

def originalData():
    import os
    dirname = os.path.dirname(__file__)
    lp = os.path.join(dirname, 'data\original\Eval ProGeo.xlsx')
    lek1 = os.path.join(dirname, 'data\original\Eval L1.xlsx')
    lek2 = os.path.join(dirname, 'data\original\Eval L2.xlsx')
    lek3 = os.path.join(dirname, 'data\original\Eval L3.xlsx')
    lek4 = os.path.join(dirname, 'data\original\Eval L4.xlsx')
    lek5 = os.path.join(dirname, 'data\original\Eval L5.xlsx')
    lek6 = os.path.join(dirname, 'data\original\Eval L6.xlsx')
    lek7 = os.path.join(dirname, 'data\original\Eval L7.xlsx')
    fps = [lp, lek1, lek2, lek3, lek4, lek5, lek6, lek7]
    return fps

def sampleData():
    import os
    dirname = os.path.dirname(__file__)
    lp = os.path.join(dirname, 'data\Eval ProGeo.xlsx')
    lp_1 = os.path.join(dirname, 'data\Eval ProGeo_p1.xlsx')
    lp_2 = os.path.join(dirname, 'data\Eval ProGeo_p2.xlsx')
    lek1 = os.path.join(dirname, 'data\Eval L1.xlsx')
    lek2 = os.path.join(dirname, 'data\Eval L2.xlsx')
    lek3 = os.path.join(dirname, 'data\Eval L3.xlsx')
    lek4 = os.path.join(dirname, 'data\Eval L4.xlsx')
    lek5 = os.path.join(dirname, 'data\Eval L5.xlsx')
    lek6 = os.path.join(dirname, 'data\Eval L6.xlsx')
    lek7 = os.path.join(dirname, 'data\Eval L7.xlsx')
    fps = [lp, lp_1, lp_2, lek1, lek2, lek3, lek4, lek5, lek6, lek7]
    return fps

def samplePath():
    import os
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'data')
    return path

def outpath(fname):
    import os
    path = samplePath()
    outpath = os.path.join(path, f'{fname}.xlsx')
    return outpath


def loadData(file = "", nrows=0):
    data = pd.read_excel(file, sheet_name="Eval")
    # colnames = data.iloc[0,:]
    # print(colnames)
    quest = data.iloc[1,:]
    # data = data[2::]
    # data.columns = colnames
    data.reset_index(inplace=True, drop=True)
    # data.index = data.iloc[:,0].astype(int)
    
    # returns all except header
    return data

def getQuestions(file="",nrows=0):
    data = pd.read_excel(file, sheet_name="Fragen")
    return data



if __name__ == "__main__":

    foo = sampleData()[0]
    bar = loadData(file=foo)
    # baz = getQuestions(file=foo)
    # print(baz)
