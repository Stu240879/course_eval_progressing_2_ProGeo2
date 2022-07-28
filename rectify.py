import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap
import re

from load import loadData, getQuestions, sampleData


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



def rectify_lessons(all=True, num:int=None):
    if all == True:
        fps = sampleData()
        fps.pop(0)
        for table in fps:
            rectify(table)
    elif num != None:
        fps = sampleData()
        rectify(fps[num])
    else:
        print("you done fucked up")

if __name__ == "__main__":
    # pd.options.display.max_colwidth = 255

    rectify_lessons(all=True)