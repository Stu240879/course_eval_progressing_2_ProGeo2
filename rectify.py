import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap
import re

from sympy import false

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

    # construct questions dataframe
    qdf = pd.DataFrame({"qid": header, "num": None, "frage": questions})
    qdf = qdf[qdf["qid"].notnull()].reset_index()

    # this will overwrite existing files!!!
    fn_out = filepath
    edf.to_excel(fn_out, sheet_name="Eval")
    with pd.ExcelWriter(fn_out, engine='openpyxl', mode='a') as writer:  
        qdf.to_excel(writer, sheet_name='Fragen')



if __name__ == "__main__":
    # pd.options.display.max_colwidth = 255

    fps = sampleData()
    print(fps)
    fps.pop(0)
    print(fps)

    for table in fps:
        print(table)
        rectify(table)