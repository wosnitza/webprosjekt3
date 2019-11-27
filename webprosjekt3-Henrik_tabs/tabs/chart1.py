import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

chart1_layout = [
    html.Div(className="main", children=[
        dcc.Graph(
            id='currGraph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2],
                        'type': 'bar', 'name': 'SF'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        ),
    ]),
    html.Button("Submit", id="testBtn"),
    html.Div(id="testDiv")
]
