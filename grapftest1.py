import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies
import Input
import Output

import pandas as pd
import plotly.graph_objs as go

# Step 1. Launch the application
app = dash.Dash()

# Step 2. Import the dataset


filepath = 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
st = pd.read_csv(filepath)

# dropdown options
features = st.columns[1: -1]
opts = [{
        'label': i,
        'value': i
        }
        for i in features
        ]

# range slider options
st['Date'] = pd.to_datetime(st.Date)
dates = ['2015-02-17', '2015-05-17', '2015-08-17', '2015-11-17',
         '2016-02-17', '2016-05-17', '2016-08-17', '2016-11-17', '2017-02-17'
         ]


# Step 3. Create a plotly figure
trace_1 = go.Scatter(x=st.Date, y=st['AAPL.High'],
                     name='AAPL HIGH',
                     line=dict(width=2,
                               color='rgb(229, 151, 50)'))
layout = go.Layout(title='Time Series Plot',
                   hovermode='closest')
fig = go.Figure(data=[trace_1], layout=layout)


# Step 4. Create a Dash layout
app.layout = html.Div([


    # adding a plot
    dcc.Graph(id='plot', figure=fig),  # dropdown
    html.P([
        html.Label("Choose a feature"),
        dcc.Dropdown(id='opt', options=opts,
                     value=opts[0])
    ], style={
        'width': '400px',
        'fontSize': '20px',
        'padding-left': '100px',
        'display': 'inline-block'
    }),  # range slider
    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id='slider',
                        marks={
                            i: dates[i]
                            for i in range(0, 9)
                        },
                        min=0,
                        max=8,
                        value=[1, 7])
    ], style={
        'width': '80%',
        'fontSize': '20px',
        'padding-left': '100px',
        'display': 'inline-block'
    })
])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
              [Input('opt', 'value'),
               Input('slider', 'value')
               ])
def update_figure(input1, input2):  # filtering the data


st2 = st[(st.Date > dates[input2[0]]) & (
    st.Date < dates[input2[1]])]  # updating the plot
trace_1 = go.Scatter(x=st2.Date, y=st2['AAPL.High'],
                     name='AAPL HIGH',
                     line=dict(width=2,
                               color='rgb(229, 151, 50)'))
trace_2 = go.Scatter(x=st2.Date, y=st2[input1],
                     name=input1,
                     line=dict(width=2,
                               color='rgb(106, 181, 135)'))
fig = go.Figure(data=[trace_1, trace_2], layout=layout)
return fig


# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug=True)
