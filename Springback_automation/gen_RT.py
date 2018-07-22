import pandas as pd
import numpy as np
import math
f1=r'C:\Users\hzoghi\Documents\2018-02\L18-Aluminum-DOE.csv'
df=pd.read_csv(f1)
df.astype(np.float64, copy=False)
factor_level={}
factors=['t','s0', 'n','k', 'r']
for factor in factors:
    level=[]
    for i in range(len(df)):
        if not df.loc[i][factor] in level:
            level.append(df.loc[i][factor])
    factor_level[factor]=level
#print(factor_level)
#generate SN values for each p-l
list_of_zeros=[0]*len(factors)
array_of_zeros=[]
for i in range(len(factor_level[factors[0]])):
    array_of_zeros.append(list_of_zeros)
df2=pd.DataFrame(array_of_zeros,columns=factors,dtype=np.float64)
df3=pd.DataFrame(array_of_zeros,columns=factors,dtype=np.float64)
dfn=pd.DataFrame(array_of_zeros,columns=factors,dtype=np.float64)
dfSN=pd.DataFrame(array_of_zeros,columns=factors,dtype=np.float64)


for factor in factors:
    for i in range(len(df)):
        for j in range(len(factor_level[factor])):
            if df.loc[i][factor] == factor_level[factor][j]:
                df2.loc[j][factor] += df.loc[i]['max_disp'] ** 2.0
                df3.loc[j][factor] += df.loc[i]['max_disp']
                dfn.loc[j][factor] +=  1

dfMean=df3/dfn

df4=df2/dfn
for i in range (len(df2)):
    for factor in factors:
        dfSN.loc[i][factor]=-10*math.log10(df4.loc[i][factor])

#add the rank values to the SN and Mean response tables
r1=[]
r2=[]
for factor in factors:
    r1.append(dfSN[factor].max()-dfSN[factor].min())
    r2.append(dfMean[factor].max()-dfMean[factor].min())
dfr1=pd.DataFrame([r1],columns=factors)
dfr2=pd.DataFrame([r2],columns=factors)
dfSN=dfSN.append(dfr1, ignore_index=True)
dfMean=dfMean.append(dfr2, ignore_index=True)

#dfSN.to_csv('AluminumSN_RT.csv')
#dfMean.to_csv('AluminumMEANs_RT.csv')
