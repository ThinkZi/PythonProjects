import pandas as pd
from vis_functions import *
from functions import find_path
import plotly as py
import os


files_list=result_files(find_path('results'))
traces=[]
layouts=[]

for res_file in files_list:
    df=pd.read_csv(res_file)
    t0, l0=get_Scatter_plot_trace_scene(df)
    traces.append(t0)
    layouts.append(l0)

titles=gen_titles(files_list)
print(files_list)
print(gen_3d_specs(4))
print(titles)
fig=gen_sub_plots(traces,layouts,titles)
py.offline.plot(fig,filename='test.html')
