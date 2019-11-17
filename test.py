# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label="Tab one", children=[
            html.Div(id="lab", className="main", children=[

                html.Div(id="boxes", children=[

                    html.Div(id="supplier", className="box", children=[
                        html.H1(children=["Supplier stats"]),
                        html.H4(children=["Input number of suppliers"]),
                        dcc.Input(id="supplierNr", type="number",
                                placeholder="Number of suppliers",),
                        html.Button("Submit", id="supplierBtn", n_clicks=0),
                        html.Div(id="supplierNrOutput", children=[

                        ]),
                        html.H4(children=['Select your used currencies']),
                        dcc.Dropdown(id="currencyChooser", options=[],
                            # {'label': k, 'value': v} for k, v in final_dict.items()],
                            placeholder="Select a currency..",
                            multi=True),
                        html.Button("Submit", id="currencyBtn"),
                        html.Div(id="currencyOutput", children=[
                            # html.Ul(id="currencyList", children=[
                            # html.Li(children=[item]) for item in list_items
                            # ]),
                        ]),
                        html.H4(children="Please input your total procurement"),
                        dcc.Input(id="procInput", type="number",
                                placeholder="Select total procurement"),
                        html.Button("Submit", id="procBtn"),
                        html.Div(id="procDiv", children=[

                        ]),


                    ]),


                    # Company section
                    html.Div(id="company", className="box", children=[
                        dcc.Input(id="companyAccounts", type="number",
                                placeholder="Number of accounts",
                                autoFocus=False),
                        html.Button("Submit", id="companyBtn", n_clicks=0),
                        html.Div(id="companyTable", children=[

                        ]),
                        # createTable()
                    ]),


                    # Customer section
                    html.Div(id="customer", className="box", children=[
                        html.H1(children=["Customer stats"]),
                        html.H4(children=["Input number of customers"]),
                        dcc.Input(id="customerNr", type="number",
                                placeholder="Number of customers"),
                        html.Button("Submit", id="customerBtn", n_clicks=0),
                        html.Div(id="customerNrOutput", children=[
                        ]),
                        html.H4(children=['Select your used currencies']),
                        dcc.Dropdown(id="currencyChooserCust", options=[],
                            # {'label': k, 'value': v} for k, v in final_dict.items()],
                            placeholder="Select a currency..",
                            searchable=True,),
                        html.Button("Submit", id="currencyBtnCust"),
                        html.Div(id="currencyOutputCust", children=[
                            # html.Ul(id="currencyList", children=[
                            # html.Li(children=[item]) for item in list_items
                            # ]),

                        ])
                    ])
                ])
            ])

        ]),
        dcc.Tab(label='Tab two', children=[
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
                ]
                ),
        ]),
        dcc.Tab(label='Tab three', children=[
                html.Div(className="main", children=[

                # dcc.Dropdown(
                # id='my-dropdown',
                # options=[
                # {'label': 'NOK', 'value': 'NOK'},
                # {'label': 'USD', 'value': 'USD'},
                # {'label': 'DKK', 'value': 'DKK'}
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
        ]),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
