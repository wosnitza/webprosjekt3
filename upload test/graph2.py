import chart-studio.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd

df = pd.read_csv('sample-data.csv')

sample_data_table = FF.create_table(df.head())
py.iplot(sample_data_table, filename='sample-data-table')

trace1 = go.Scatter(
    x=df['x'], y=df['logx'],  # Data
    mode='lines', name='logx'  # Additional options
)
trace2 = go.Scatter(x=df['x'], y=df['sinx'], mode='lines', name='sinx')
trace3 = go.Scatter(x=df['x'], y=df['cosx'], mode='lines', name='cosx')

layout = go.Layout(title='Simple Plot from csv data',
                   plot_bgcolor='rgb(230, 230,230)')

fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

# Plot data in the notebook
py.iplot(fig, filename='simple-plot-from-csv')
