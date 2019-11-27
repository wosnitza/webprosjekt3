import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

chart2_layout = [
    html.Div(className="main", children=[

        # dcc.Dropdown(
        # id='my-dropdown',
        # options=[
        #{'label': 'NOK', 'value': 'NOK'},
        #{'label': 'USD', 'value': 'USD'},
        #{'label': 'DKK', 'value': 'DKK'}
        # ],
        # value='USD'
        # ),

        dcc.Graph(
            id='graph',
            config={
                'showSendToCloud': True,
                'plotlyServerURL': 'https://plot.ly'
            }
        ),
    ])
]
