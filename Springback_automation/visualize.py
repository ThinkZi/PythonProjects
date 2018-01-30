import pandas as pd
from vis_functions import *
from functions import find_path
import plotly as py


files_list=result_files(find_path('results'))
traces=[]
layouts=[]

for res_file in files_list:
    df=pd.read_csv(res_file)
    t0, l0=get_Scatter_plot_trace_scene(df)
    traces.append(t0)
    layouts.append(l0)


fig=gen_sub_plots(traces,layouts)
py.offline.plot(fig,filename='test.html')
