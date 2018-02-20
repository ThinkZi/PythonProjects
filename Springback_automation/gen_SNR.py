import pandas as pd
f1=r'C:\Users\hzoghi\Documents\2018-02\L18-Aluminum-DOE.csv'
df=pd.read_csv(f1)
n=0
factor_level={}
factors=['t','s0', 'n','k', 'r']
for factor in factors:
    level=[]
    for i in range(len(df)):
        if not df.iloc[i][factor] in level:
            level.append(df.iloc[i][factor])
    factor_level[factor]=level

#generate SN values for each p-l
