import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

from load import loadData, getQuestions, sampleData


# pd.options.display.max_colwidth = 255

# columns
time_cols = 18
time_labels = ["0-30","30-60","60-120","120-180","180-240","240+", "kA"]



# columns are reversed (6-1)
reversed_cols = [11,12,13,14,15,16,17]
# columns are shifted by -1 (0-5) all others are (1-6)
shifted_cols = [9,10]


def df_to_int(df):
    # all columns except col=0 
    cols = range(1, df.shape[1])
    for col in cols:
        df.iloc[:,col] = df.iloc[:,col].fillna(0).astype(int)

    return df

def reverse_coldata(df, cols):
    df = df_to_int(df)
    # ist = [1,2,3,4,5,6]
    soll = [0,6,5,4,3,2,1]
    for col in cols:
        d = df.iloc[:,col].values.tolist()
        r = [soll[n] for n in d]
        df.iloc[:,col] = r
    return df

def shift_coldata(df, cols):
    for col in cols:
        d = df.iloc[:,col].values.tolist()
        r = [n+1 if n>0 else n for n in d ]
        df.iloc[:,col] = r
    return df


if __name__ == "__main__":



    # get Data
    fps = sampleData()
    # survey_fp = fps.pop(1)
    surveys = fps[1:]
    print(surveys)

    # print(q_df)

    ### Processing Dataframes
    data = []
    for lesson in surveys:
        q_df = getQuestions(file=lesson)
        d_df = loadData(file=lesson)

        # drop column with text. 
        # here: last column 
        d_df.drop(columns=d_df.columns[-1], 
                axis=1, 
                inplace=True)

        df_rev = reverse_coldata(d_df, reversed_cols)
        df = shift_coldata(df_rev, shifted_cols)
        df["4.1.1"] = [time_labels[n-1] for n in df.iloc[:,-1]]

        data.append(df)
        # print(f'df for lesson {lesson}')
        # print(df)
        # print("\n")


    print(len(data))

    ### charting
# set options
pd.options.display.max_colwidth = 255


print(q_df)


qids = q_df["qid"]

for qid in qids: 
    cols = []
    for df in data:
        cols.append(df[str(qid)])
    print(cols)



### Stuff

# # split 
# coltype = "int"
# cols = list(q_df[q_df["type"] == coltype]["num"])
# qual = [i+1 for i in cols]
# text = [i for i in range(1,45,1) if i not in qual]

# # replace all NaN with zeros
# data = d_df.fillna(0)

# # get  skill level from first question
# # replace this
# skill_strlist = list(map(lambda x: x.replace('Ja', 'True' ).replace('Nein', 'False'), data.iloc[:,text]["1.1"].to_list()))
# skill = [elem == "True" for elem in skill_strlist]


# def splitGroup(data, skill:list):
#     # get unskilled participants by flipping values
#     unskill = [not elem for elem in skill]
#     groups = [data.iloc[skill,:], data.iloc[unskill,:]]
#     return groups


# part_groups_qual = splitGroup(data.iloc[:,qual], skill)
# part_groups_text = splitGroup(data.iloc[:,text], skill)

# textstr = "1: sehr schlecht - 2: schlecht - 3: ok - 4: gut - 5: sehr gut - kA: keine Angabe"

# qids = list(part_groups_qual[0].columns)


# for qid in qids:

#     dirname = os.path.dirname(__file__)
#     fp_out = os.path.join(dirname, f'charts\chart_{qid}.png')
#     question = q_df[q_df["qid"] == qid]["frage"].to_string(index=False)
    
#     print(f'generating: {fp_out} for question {qid}')

    

#     # qid = "2.1"
#     stacked = False

#     gA = part_groups_qual[0][qid].tolist()
#     gB = part_groups_qual[1][qid].tolist()

#     x = [gA,gB]

#     groups = ["skilled","unskilled"]
#     xlabels = ['kA', '1 \n trifft nicht zu', '2', '3', '4', '5 \n trifft voll zu']
#     title = "Institut für Sphärische Konjugation"
#     colors = ['blue', 'orange']#, 'lime']

#     fig, ((ax0)) = plt.subplots()

#     if stacked == True:
#         ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', stacked=True,  color=colors, align='mid', label=groups)
#         ax0.set_title('stacked')
#     else:
#         ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', color=colors, label=groups, width = 0.4)
#         ax0.set_title("\n".join(wrap(f'{question}', 50)), fontsize=12)
#     ax0.set_ylabel('Anzahl TN')
#     ax0.legend(prop={'size': 10})

#     ax0.set_xticks([0,1,2,3,4,5], xlabels)

#     fig.suptitle("\n".join(wrap(f'{str(qid)}', 50)), fontsize=16)
#     fig.tight_layout()
#     plt.savefig(fp_out)