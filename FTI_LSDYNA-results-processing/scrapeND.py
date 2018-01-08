import pandas as pd
import os
import re
from plotly.offline import plot, layout, Scatter

#lists the files containing relevant data in the folder
def listfiles():
    allfilelist=os.listdir()
    ndfilelist=[]
    for f in allfilelist:
        if f.endswith('ND.txt'):
            ndfilelist.append(f)
    return ndfilelist

#reads the nodal displacement files and creates a list of the lines containing
# the node id and displacement in coordinates ["NID Xdisp Ydisp Zdisp"]
def makeNDlist(fname):
    NDlist=[]
    skipSymbols=['$','*']
    with open(fname) as f:
        for line in f:
            if not line[0] in skipSymbols:
                NDlist.append(line)
    return NDlist

#converts the nodal displacement list to a dictionary
#{"NID1": ["Xdisp1", "Ydisp1", "Zdisp1"], "NID2: [...]"}
def makeNDdict(ndlist):
    NDdict={}
    for l in ndlist:
        NDdict[l.split()[0]]=l.split()[1:]
    return NDdict

#converts the nodal displacement dictionary to a pandas DataFrame
#with node IDs as index and 'x','y','z' as column names
#plus it adds a new column called 'dist' which is the absolute nodal displacement
def makeNDdf(nddict):
    NDdf=pd.DataFrame.from_dict(nddict, orient="index")
    NDdf=NDdf.astype(float)
    NDdf.columns=['x','y','z']
    NDdf["dist"]=(NDdf.x**2+NDdf.y**2+NDdf.z**2)**0.5
    return NDdf

#Uses all the functions above to create pandas DataFrame from the original file
def convertfiletoDF(fname):
    df=makeNDdf(makeNDdict(makeNDlist(fname)))
    E=re.findall('\d+',fname)
    df['YoungModulus']=(E[0])
    return df

#Show the scatter plot using bokeh
def visualize(df, yname):
    fig={
    'data': [
        {
        'x':df.index,
        'y':df[yname]
        }
    ],
    'layout':{
        'xaxis':{'title': 'Young Modulus'},
        'yaxis':{'title': 'Max displacement'}
    }
    }
    plot(fig, filename='SpringBack-YoungModulus')
    return

#main workflow
def main():
    flist=listfiles()
    results={}
    for f in flist:
        DF1=convertfiletoDF(f)
        maxDisp=DF1.dist.max(0)
        E=DF1.iloc[int(DF1.dist.idxmax(0))]['YoungModulus']
        results[int(E)]=maxDisp
    DF2=pd.DataFrame.from_dict(results,orient='index')
    DF2=DF2.sort_index()
    DF2.index.name='E'
    DF2.columns=['displacement']
    print(DF2)
    DF2.to_csv('results.csv')
    visualize(DF2,'displacement')
    return
main()
