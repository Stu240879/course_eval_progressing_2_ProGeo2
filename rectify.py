import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap
import re

from sympy import false

from load import loadData, getQuestions, sampleData

fps = sampleData()
fps.pop(0)


testdata = fps[0]
table = pd.read_excel(testdata)

table_head = table.columns
q_len = len(table_head)
print(q_len)




head = list(table_head)


if __name__ == "__main__":
    pd.options.display.max_colwidth = 255
    i = 0
    header = []
    questions = []

    print(head)
    tmp = head[len(head)-2]
    head[len(head)-2] = head[len(head)-1] 
    head[len(head)-1] = tmp
    print(head)



    for row in head:
        i+=1
        x= False
        if re.match('\A([0-9].[0-9])', row) == None: 
            num = None
            qu = None
        else:
             strlist = re.split('\A([0-9].[0-9])', row)
             num = strlist[1]
             qu = strlist[2].lstrip()

        print(i, num, x)
        header.append(num)
        questions.append(qu)


    
    table.columns = header

    df2 = pd.DataFrame({"qid": header, "frage": questions})
    print(df2)

    print(table.columns)

    table.to_excel('data/foo.xlsx', sheet_name="Eval")

    with pd.ExcelWriter('data/foo.xlsx', engine='openpyxl', mode='a') as writer:  
        df2.to_excel(writer, sheet_name='Fragen')
        