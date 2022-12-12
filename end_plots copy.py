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
cols_num = list(q_df[q_df["type"] == "int"].index)
cols_bool = list(q_df[q_df["type"] == "bool"].index)
cols_text = list(q_df[q_df["type"] == "text"].index)



# replace bool fields (ja/nein, Land/Kommune) with T/F
# for col in [2]:
for col in cols_bool:
    # print(f'\n\nreplacing col {col}: {q_df.iloc[col,:]}')
    if d_df.iloc[:,col].name == "A.1" or d_df.iloc[:,col].name == "4.7":
        d_df.iloc[:,col] = list(map(lambda x: str(x).replace('1', 'True' ).replace('0', 'False').replace('2', 'kA'), d_df.iloc[:,col].to_list()))
    else:
        d_df.iloc[:,col] = list(map(lambda x: str(x).replace('Ja', 'True' ).replace('Nein', 'False'), d_df.iloc[:,col].to_list()))



# replace all NaN with zeros
data = d_df.fillna(0)
print(data)
# data.to_excel("bar.xlsx")


# make partition lists for skilled / unskilled users and users on landesebene and kommunalebene
# skill_strlist = list(map(lambda x: x.replace('Ja', 'True' ).replace('Nein', 'False'), data.iloc[:,cols_bool]["1.1"].to_list()))
#  ^^^ no longer needed....i think
# skill = [elem == "True" for elem in d_df.iloc[:,cols_bool]["1.1"]]
# ebene = [elem == "True" for elem in d_df.iloc[:,cols_bool]["A.1"]]


# partition list for skill and anstellungsebene
skill = [elem == "True" for elem in data.iloc[:,cols_bool]["1.1"]]
ebene = [elem == "False" for elem in data.iloc[:,cols_bool]["A.1"]]

print(skill)
print(ebene)

### returns a list of two dataframes, partitioned by list of bool values
def splitGroup(data, partition:list):
    # get unskilled participants by flipping values
    unpartition = [not elem for elem in partition]
    groups = [data.iloc[partition,:], data.iloc[unpartition,:]]
    return groups


part_groups_qual_skill = splitGroup(data.iloc[:,cols_num], skill)
part_groups_bool_skill = splitGroup(data.iloc[:,cols_bool], skill)
part_groups_bool_ebene = splitGroup(data.iloc[:,cols_bool], ebene)
part_groups_text = splitGroup(data.iloc[:,cols_text], skill)



print("\nqual-skill")
print(part_groups_qual_skill)
print("\nbool-skill")
print(part_groups_bool_skill)
print("\nbool-ebene")
print(part_groups_bool_ebene)



# # this is no longer used
# qualstr = "1: sehr schlecht - 2: schlecht - 3: ok - 4: gut - 5: sehr gut - kA: keine Angabe"
# boolstr = "1: Ja - 2: Nein - kA: keine Angabe"
# timestr = "1:  - 2:  - kA: keine Angabe"
# # ===


### make qual diagrams (NA, 1-5)
qids = list(part_groups_qual_skill[0].columns)

for qid in qids:

    dirname = os.path.dirname(__file__)
    fp_out = os.path.join(dirname, f'charts\chart_{qid}.png')
    question = q_df[q_df["qid"] == qid]["frage"].to_string(index=False)
    
    print(f'generating: {fp_out} for question {qid}')

    stacked = False

    gA = part_groups_qual_skill[0][qid].tolist()
    gB = part_groups_qual_skill[1][qid].tolist()

    x = [gA,gB]

    skill_groups = ["mit Vorkenntnissen","ohne Vorkenntnisse"] #["skilled","unskilled"]
    xlabels = ['kA', '1 \n trifft nicht zu', '2', '3', '4', '5 \n trifft voll zu']

    title = "Institut für Sphärische Konjugation"
    colors = ['blue', 'orange']#, 'lime']

    fig, ((ax0)) = plt.subplots()

    if stacked == True:
        ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', stacked=True,  color=colors, align='mid', label=skill_groups)
        ax0.set_title('stacked')
    else:
        ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', color=colors, label=skill_groups, width = 0.4)
        ax0.set_title("\n".join(wrap(f'{question}', 50)), fontsize=12)
    ax0.set_ylabel('Anzahl TN')
    ax0.legend(prop={'size': 10})

    ax0.set_xticks([0,1,2,3,4,5], xlabels)

    fig.suptitle("\n".join(wrap(f'{str(qid)}', 50)), fontsize=16)
    fig.tight_layout()
    plt.savefig(fp_out)
    plt.clf()
    plt.cla()
    plt.close()



### make qual diagrams (Ja/Nein)


def makeHist_YN_grouped(preppedDF:pd.DataFrame, group_descriptor:list=["keine angaben", "keine angaben"]):
    
    qids_bool = list(preppedDF[0].columns)
    
    for qid in qids_bool:

        dirname = os.path.dirname(__file__)
        fp_out = os.path.join(dirname, f'charts\chart_{qid}.png')
        question = q_df[q_df["qid"] == qid]["frage"].to_string(index=False)
        
        print(f'generating: {fp_out} for question {qid}')
        stacked = False
        ### why did i have to switch this here?
        gA = preppedDF[0][qid].tolist()
        gB = preppedDF[1][qid].tolist()

        x = [gA,gB]



        group_description = ['mit Vorkenntnissen','ohne Vorkenntnisse']
        skill_groups = group_descriptor
        xlabels_bool = ['0 \nNein','1 \nJa', 'kA \nunentschlossen']
        colors = ['blue', 'orange']#, 'lime']
        fig, ((ax0)) = plt.subplots()
        if stacked == True:
            ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', stacked=True,  color=colors, align='mid', label=skill_groups)
            ax0.set_title('stacked')
        else:
            ax0.hist(x, bins=[-0.5,0.5,1.5,2.5], density=False, histtype='bar', color=colors, label=skill_groups, width = 0.4)
            ax0.set_title("\n".join(wrap(f'{question}', 50)), fontsize=12)
        ax0.set_ylabel('Anzahl TN')
        ax0.legend(prop={'size': 10})

        ax0.set_xticks([0,1,2], xlabels_bool)

        fig.suptitle("\n".join(wrap(f'{str(qid)}', 50)), fontsize=16)
        fig.tight_layout()
        plt.savefig(fp_out)
        plt.clf()
        plt.cla()
        plt.close()


for qid in ["1.1", "2.5"]:

    dirname = os.path.dirname(__file__)
    fp_out = os.path.join(dirname, f'charts\chart_{qid}_a.png')
    question = q_df[q_df["qid"] == qid]["frage"].to_string(index=False)
    
    print(f'generating: {fp_out} for question {qid}')

    stacked = False

    gA = part_groups_bool_ebene[0][qid].tolist()
    gB = part_groups_bool_ebene[1][qid].tolist()

    x = [gA,gB]

    skill_groups = ['mit Vorkenntnissen','ohne Vorkenntnisse']
    ebene_groups = ['Kommunalbedienstete', 'Landesbedienstete']
    xlabels_bool = ['0 \nNein','1 \nJa', 'kA \nunentschlossen']

    title = "Institut für Sphärische Konjugation"
    colors = ['blue', 'orange']#, 'lime']

    fig, ((ax0)) = plt.subplots()

    if stacked == True:
        ax0.hist(x, bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], density=False, histtype='bar', stacked=True,  color=colors, align='mid', label=ebene_groups)
        ax0.set_title('stacked')
    else:
        ax0.hist(x, bins=[-0.5,0.5,1.5,2.5], density=False, histtype='bar', color=colors, label=ebene_groups, width = 0.4)
        ax0.set_title("\n".join(wrap(f'{question}', 50)), fontsize=12)
    ax0.set_ylabel('Anzahl TN')
    ax0.legend(prop={'size': 10})

    ax0.set_xticks([0,1,2], xlabels_bool)

    fig.suptitle("\n".join(wrap(f'{str(qid)}', 50)), fontsize=16)
    fig.tight_layout()
    plt.savefig(fp_out)
    plt.clf()
    plt.cla()
    plt.close()



if __name__ == "__main__":
    
    # prepareDataframes(filename)

    makeHist_YN_grouped(part_groups_bool_skill)
    makeHist_YN_grouped(part_groups_bool_ebene)

