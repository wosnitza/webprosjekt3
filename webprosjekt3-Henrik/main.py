import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from data import final_dict

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Show FX lab', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

stats_layout = html.Div(className="main", children=[
    html.Img(id="logo", src="/assets/logo.png"),

    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

    html.Div(id="lab", children=[

        html.Div(id="boxes", children=[

            html.Div(id="supplier", className="box", children=[
                html.H1(children=["Supplier stats"]),
                html.H4(children=["Input number of suppliers"]),
                dcc.Input(id="supplierNr", type="number",
                          placeholder="Number of suppliers",
                          autoFocus=False),
                html.Button("Submit", id="supplierBtn", n_clicks=0),
                html.Div(id="supplierNrOutput", children=[

                ]),
                html.H4(children=['Select your used currencies']),
                dcc.Dropdown(id="currencyChooser", options=[
                    {'label': k, 'value': v} for k, v in final_dict.items()],
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

            html.Div(id="company", className="box", children=[
                html.P(children=["Heisann heisann kær"]),
            ]),

            html.Div(id="customer", className="box", children=[

            ])
        ])
    ])
])


@app.callback(
    dash.dependencies.Output("supplierNrOutput", "children"),
    [dash.dependencies.Input("supplierBtn", "n_clicks")],
    [dash.dependencies.State("supplierNr", "value")]
)
def showSupplierNr(n_clicks, value):
    return [
        "You have {} customers!".format(
            value) if value and value > 0 else "Please select your number of customers!"
    ]


@app.callback(
    dash.dependencies.Output("currencyOutput", "children"),
    [dash.dependencies.Input("currencyBtn", "n_clicks")],
    [dash.dependencies.State("currencyChooser", "value")]
)
def addCurrency(n_clicks, value):
    result_divs = []
    result_divs.append(
        html.P(children="Select how each currency influences your procurement in %"))
    if value:
        result_divs.append(html.Button(("Submit"), id="currPercentBtn"))
        for i in value:
            result_divs.append(html.Div(id="currDiv" + str(i), children=[
                html.Li(id="currLi" + str(i), children=[i]),
                dcc.Input(id="currInput" + str(i),
                          className="currInputs", type="number")
            ])
            )
        return result_divs
    else:
        return html.P(children="Please select your used currencies!")
    #i += 1
    # for o in range(i):
        #o += 1
        # return html.Div(id="currDiv" + str(o), children=[
        #html.Li(id="currLi" + str(o), children=[value]),
        #dcc.Input(id="currInput" + str(o), type="number")
        # ])


@app.callback(
    dash.dependencies.Output("currGraph", "figure"),
    [dash.dependencies.Input("currPercentBtn", "n_clicks"),
    dash.dependencies.Input("currencyChooser", "value")],
    [dash.dependencies.State("currencyInputs", "value")]
)
def createCurrencyGraph(n_clicks, value1, value2):
    fig = {}
    fig = {'data': [{'x':[i for i in value1],'y':[i for i in value2],'type':'bar','name': 'update'}]}
    return fig
# for i in stats_layout['currencyOutput'].children


@app.callback(
    dash.dependencies.Output("procDiv", "children"),
    [dash.dependencies.Input("procBtn", "n_clicks")],
    [dash.dependencies.State("procInput", "value")]
)
def showProc(n_clicks, value):
    if value:
        return "Total procurement: {}".format(value)
    else:
        return "Please input your total procurement!"


graphs_layout = html.Div(className="main", children=[

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
    html.Div(id="currGraphDiv", children=[

    ]),
    dcc.Graph(
        id='currGraph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),







    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return stats_layout
    elif pathname == '/page-2':
        return graphs_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
