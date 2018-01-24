import pandas as pd
import os
import plotly as py
from plotly.graph_objs import Scatter3d, Layout, Figure
def result_files(topdir):
    flist=[]
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            flist.append(os.path.join(dirpath, name))
    return flist

def get_Scatter_plot(dframe):
    #these strings e.g. x-coor , x-disp are coming from the dumped csv file
    #which in turn is coming from the DYNA nodout file
    xt="x-coor"
    yt="y-coor"
    zt="z-coor"
    abs_disp=(dframe['x-disp']**2+dframe['y-disp']**2+dframe['z-disp']**2)**(0.5)
    axis_range=set_axis_ranges(dframe)
    trace=Scatter3d(x=dframe[xt].values,y=dframe[yt].values,z=dframe[zt].values,
    mode='markers',
    marker=dict(size=3,color=abs_disp,colorscale='Jet',showscale=True),
    legendgroup=abs_disp,
    hovertext=abs_disp)
    data=[trace]
    layout=Layout(scene=dict(xaxis=dict(range=axis_range[xt]),
    yaxis=dict(range=axis_range[yt]),
    zaxis=dict(range=axis_range[zt])),
    margin=dict(l=0,r=0,b=0,t=0))
    fig=Figure(data=data,layout=layout)
    return fig

def set_axis_ranges(dframe):
    axes=['x-coor','y-coor','z-coor']
    max_range=0
    axis_range={}
    for axis in axes:
        _range=dframe.max()[axis]-dframe.min()[axis]
        if _range > max_range:
            max_range = _range
    for axis in axes:
        center=(dframe.min()[axis]+dframe.max()[axis])/2
        lower=int(center-max_range/2)-1
        upper=int(center+max_range/2)+1
        axis_range[axis]=[lower,upper]
    return axis_range

#df=pd.read_csv(r'C:\Hamed\test.csv')
#fig=get_Scatter_plot(df)
#py.offline.plot(fig,filename='test.html')
