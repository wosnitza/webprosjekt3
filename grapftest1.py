import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

filepath = 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
st = pd.read_csv(filepath)


# Step 3. Create a plotly figure
trace_1 = go.Scatter(x=st.Date, y=st['AAPL.High'],
                     name='AAPL HIGH',
                     line=dict(width=2,
                               color='rgb(229, 151, 50)'))
layout = go.Layout(title='Le epic graf',
                   hovermode='closest')
fig = go.Figure(data=[trace_1], layout=layout)


# Step 4. Create a Dash layout
app.layout = html.Div([

    # adding a plot
    dcc.Graph(id='plot', figure=fig),
])

# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug=True)
