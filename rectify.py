import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap
import re

from load import loadData, getQuestions, originalData, sampleData, outpath


def rect_LPeval(filepath):
    # load data
    evaldf = pd.read_excel(filepath)
    evaldf_head = evaldf.columns
    headerList = list(evaldf_head)
    names = headerList
    
    # init
    i = 0
    header = []
    questions = []

    # move col_name right
    rMove = [11,50,57,59,67,69,71,74,77]
    for ncol in rMove:
        names[ncol] = names[ncol-1]
        names[ncol-1] = "empty"


    # move col_name left
    lMove = [12,22]
    for ncol in lMove:
        names[ncol] = names[ncol+1]
        names[ncol+1] = "empty"

    # delete columns
    delete_cols = [2,3,4,5,6]
    
    # split questions from numbers and store in separate lists
    for n in names:
        i+=1
        if re.match('\A([0-9|A-Z].[0-9])', n) == None: 
            num = None
            qu = None
        elif re.match('\A([A-Z].[0-9])', n) != None:
            strlist = re.split('\A([A-Z].[0-9])', n)
            num = strlist[1]
            qu = strlist[2].lstrip()
        elif re.match('\A([0-9].[0-9].[0-9])', n) != None:

            strlist = re.split('\A([0-9].[0-9].[0-9])', n)
            num = strlist[1]
            qu = strlist[2].lstrip()
        elif re.match('\A([0-9].[0-9])', n) != None:
            strlist = re.split('\A([0-9].[0-9])', n)
            num = strlist[1]
            qu = strlist[2].lstrip()
        else:
            print(f'you done fucked up at col {i}')
    
        header.append(num)
        questions.append(qu)
    
    # make new table header from qid
    header[0] = "A.0 Nutzer"
    header[1] = "A.0 Abgabedatum"

    evaldf.columns = header

    ### check if whole col is na and delete
    ### !!! This will delete all columns where there is no data....even if you want it to be NA !!!
    evaldf = evaldf.dropna(axis=1,how='all')


    # construct questions dataframe
    qdf = pd.DataFrame({"qid": header, "num": None, "type": None, "frage": questions})
    qdf = qdf[qdf["qid"].notnull()].reset_index()

    # this will overwrite existing files!!!
    fn_out = sampleData()[0]
    evaldf.to_excel(fn_out, sheet_name="Eval", index=False)
    with pd.ExcelWriter(fn_out, engine='openpyxl', mode='a') as writer:  
        qdf.to_excel(writer, sheet_name='Fragen')
    print("Excel file created")




def rectify(filepath):
    edf = pd.read_excel(filepath)

    edf_head = edf.columns
    q_len = len(edf_head)

    head = list(edf_head)
    i = 0
    header = []
    questions = []

    # swap columns for last question
    tmp = head[len(head)-2]
    head[len(head)-2] = head[len(head)-1] 
    head[len(head)-1] = tmp

    for row in head:
        i+=1
        x = False
        if re.match('\A([0-9].[0-9])', row) == None: 
            num = None
            qu = None
        else:
             strlist = re.split('\A([0-9].[0-9])', row)
             num = strlist[1]
             qu = strlist[2].lstrip()
    
        # make new table header
        header.append(num)
        questions.append(qu)

    edf.columns = header
    edf = edf.dropna(axis=1,how='all')

    # construct questions dataframe
    qdf = pd.DataFrame({"qid": header, "num": None, "type": None, "frage": questions})
    qdf = qdf[qdf["qid"].notnull()].reset_index()

    # this will overwrite existing files!!!
    fn_out = filepath
    edf.to_excel(fn_out, sheet_name="Eval", index=False)
    with pd.ExcelWriter(fn_out, engine='openpyxl', mode='a') as writer:  
        qdf.to_excel(writer, sheet_name='Fragen')



def rectify_LESeval(all=True, num:int=None):
    if all == True:
        fps = sampleData()
        fps.pop(0)
        for table in fps:
            rectify(table)
    elif num != None:
        fps = sampleData()
        rectify(fps[num])
    else:
        print("you dun fucked up")

if __name__ == "__main__":
    # pd.options.display.max_colwidth = 255
    # rectify_LESeval(all=True)
    
    fps = originalData()
    fp_in = fps[0]
    rect_LPeval(fp_in)