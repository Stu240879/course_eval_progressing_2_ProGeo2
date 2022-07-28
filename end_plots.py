import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap

from load import loadData, getQuestions, sampleData



pd.options.display.max_colwidth = 255

# get Data
fps = sampleData()
# get first xlsx only
survey_fp = fps.pop(0)
q_df = getQuestions(file=survey_fp)
d_df = loadData(file=survey_fp)

# split 
coltype = "int"
cols = list(q_df[q_df["type"] == coltype]["num"])
qual = [i+1 for i in cols]
text = [i for i in range(1,45,1) if i not in qual]


# replace all NaN with zeros
data = d_df.fillna(0)

# get  skill level from first question
# replace this
skill_strlist = list(map(lambda x: x.replace('Ja', 'True' ).replace('Nein', 'False'), data.iloc[:,text]["1.1"].to_list()))
skill = [elem == "True" for elem in skill_strlist]


def splitGroup(data, skill:list):
    # get unskilled participants by flipping values
    unskill = [not elem for elem in skill]
    groups = [data.iloc[skill,:], data.iloc[unskill,:]]
    return groups


part_groups_qual = splitGroup(data.iloc[:,qual], skill)
part_groups_text = splitGroup(data.iloc[:,text], skill)

textstr = "1: sehr schlecht - 2: schlecht - 3: ok - 4: gut - 5: sehr gut - kA: keine Angabe"

qids = list(part_groups_qual[0].columns)


for qid in qids:

    dirname = os.path.dirname(__file__)
    fp_out = os.path.join(dirname, f'charts\chart_{qid}.png')
    question = q_df[q_df["qid"] == qid]["frage"].to_string(index=False)
    
    print(f'generating: {fp_out} for question {qid}')

    

    # qid = "2.1"
    stacked = False

    gA = part_groups_qual[0][qid].tolist()
    gB = part_groups_qual[1][qid].tolist()

    x = [gA,gB]

    groups = ["skilled","unskilled"]
    xlabels = ['kA', '1 \n trifft nicht zu', '2', '3', '4', '5 \n trifft voll zu']
    title = "Institut für Sphärische Konjugation"
    colors = ['blue', 'orange']#, 'lime']

    fig, ((ax0)) = plt.subplots()

    if stacked == True:
        ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', stacked=True,  color=colors, align='mid', label=groups)
        ax0.set_title('stacked')
    else:
        ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', color=colors, label=groups, width = 0.4)
        ax0.set_title("\n".join(wrap(f'{question}', 50)), fontsize=12)
    ax0.set_ylabel('Anzahl TN')
    ax0.legend(prop={'size': 10})

    ax0.set_xticks([0,1,2,3,4,5], xlabels)

    fig.suptitle("\n".join(wrap(f'{str(qid)}', 50)), fontsize=16)
    fig.tight_layout()
    plt.savefig(fp_out)