from plotly.offline import plot
from plotly.graph_objs import Scatter, Scatter3d, Layout, Mesh3d
import pandas as pd

df=pd.read_csv('out.csv')
data=[Scatter3d(x=df['x'],y=df['y'],z=df['z'], text=df['result'],mode="markers",
    marker={"color":df['result'],"colorscale":"Jet","showscale":True,"size":4})]
#print(min(df['x']), max(df['x']))
#print(min(df['y']), max(df['y']))
#print(min(df['z']), max(df['z']))
layout=Layout(scene=dict(xaxis={"range":[300,1600]}, yaxis={"range" : [-1500,-200]}, zaxis={"range" : [-1250,800]}))
figure={"data":data, "layout":layout}
plot(figure)
