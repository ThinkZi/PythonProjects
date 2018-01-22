import pandas as pd
import os
from functions import read_nodout_to_df, return_nodout_file_paths, find_path

raw_simulation_data_folder=find_path('ArchivedDynaOutputs')
files_list=return_nodout_file_paths(raw_simulation_data_folder)
results_folder=find_path('results')
i=0
for f in files_list:
    i+=1
    df=read_nodout_displacements_to_df(f)
    df.to_csv(results_folder+"/test"+str(i)+".csv")
