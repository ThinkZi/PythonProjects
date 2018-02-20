from vis_functions import result_files
import pandas as pd
flist= result_files(r'C:\Hamed\backup\test\Springback_Experiment\filleted\IDDRG2018\Aluminum\results')
disp=[]
simID=[]
for f in flist:
    df=pd.read_csv(f)
    df['disp']=(df['x-disp']**2+df['y-disp']**2+df['z-disp']**2)**(0.5)
    disp.append(df['disp'].max())
    simID.append(f[-9:-4])
df2=pd.DataFrame({'simID': simID, 'max_displacement':disp})
print(df2)
df2.to_csv('max_disp.csv')
