import dash
import base64
import datetime
import io
import dash_table

import dash_bootstrap_components as dbc

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from data.mockaroo import createTable
from data.data import final_dict

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
filepath = 'test.csv'
st = pd.read_csv(filepath)

# Creates a table and sets headers to loook for
trace_1 = go.Scatter(x=st.Date, y=st['AAPL.High'],
                     name='AAPL HIGH',
                     line=dict(width=2,
                               color='rgb(229, 151, 50)'))
layout = go.Layout(title='Graph',
                   hovermode='closest')
fig = go.Figure(data=[trace_1], layout=layout)


app.config.suppress_callback_exceptions = True


app.layout = html.Div(className="main", children=[
    html.Img(id="logo", src="/assets/logo.png"),

    html.Div(id="infoDiv", style={"display": "none"}),

    html.Div(id="appLayout"),

    html.Div(id="lab", className="main", children=[

        html.Div(className="menu", children=[
        html.Button('Menu1', id="vbutton1"),
        html.Button('Menu2', id="vbutton2"),
        html.Button('Menu3', id="vbutton3"),
        ]),
        dcc.Graph(id='plot', figure=fig),

        html.Div(
            id="boxes",

            style={
                'display': 'none'
            },
            children=[

            html.Div(
                id="supplier",
                className="box",
                children=[

                    html.H1(children=["Supplier stats"]),
                    html.H4(children=["Input number of suppliers"]),
                    dcc.Input(
                        id="supplierNr",
                        type="number",
                        placeholder="Number of suppliers",
                        autoFocus=False),
                    html.Br(),
                    html.Button(
                        "Submit",
                        id="supplierBtn",
                        n_clicks=0),

                    html.Div(
                        id="supplierNrOutput",
                        children=[
                        ]),

                    html.H4(children=['Select your used currencies']),
                    dcc.Dropdown(
                        id="currencyChooser",
                        options=[

                        {'label': k, 'value': v} for k, v in final_dict.items()],

                        placeholder="Select a currency..",
                        multi=True),
                    html.Button(
                        "Submit",
                        id="currencyBtn"),
                    html.Div(
                        id="currencyOutput",
                        children=[
                        # html.Ul(id="currencyList", children=[
                        # html.Li(children=[item]) for item in list_items
                        # ]),
                    ]),
                    html.H4(
                        children="Please input your total procurement"),
                    dcc.Input(
                        id="procInput",
                        type="number",
                        placeholder="Select total procurement"),
                    html.Br(),
                    html.Button(
                        "Submit",
                        id="procBtn"),
                    html.Div(
                        id="procDiv",
                        children=[

                    ]),
                ]),

            # Company section
            html.Div(
                id="company",
                className="box",
                children=[
                html.H1(children=["Number of accounts"]),
                html.H4(children=["Input number of accounts"]),
                dcc.Input(
                    id="companyAccounts",
                    type="number",
                    placeholder="Number of accounts",
                    autoFocus=False),
                html.Br(),
                html.Button(
                    "Submit",
                    id="companyBtn",
                    n_clicks=0),
                html.Div(
                    id="companyTable",
                    children=[

                ]),
                # createTable()
            ]),


            # Customer section
            html.Div(id="customer", className="box", children=[
                html.H1(children=["Customer stats"]),
                html.H4(children=["Input number of customers"]),
                dcc.Input(id="customerNr", type="number",
                          placeholder="Number of customers",
                          autoFocus=False),
                html.Br(),
                html.Button("Submit", id="customerBtn", n_clicks=0),
                html.Div(id="customerNrOutput", children=[
                ]),
                html.H4(children=['Select your used currencies']),
                dcc.Dropdown(id="currencyChooserCust", options=[
                    {'label': k, 'value': v} for k, v in final_dict.items()],
                    placeholder="Select a currency..",
                    searchable=True),
                html.Button("Submit", id="currencyBtnCust"),
                html.Div(id="currencyOutputCust", children=[
                    # html.Ul(id="currencyList", children=[
                    # html.Li(children=[item]) for item in list_items
                    # ]),

                ])
            ])
        ])
    ]),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),

    html.Div(className="main", children=[
        dcc.Graph(
            id='currGraph',
            style={
                'display': 'none'
            },
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

#    html.Div(className="main", children=[
#
#       dcc.Graph(
#            id='graph',
#            config={
#                'showSendToCloud': True,
#                'plotlyServerURL': 'https://plot.ly'
#            }
#       ),
#    ]),
])


# CALLBACKS:


def parse_contents(contents, filename, date):
    content_type, content_string=contents.split(',')

    decoded=base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df=pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df=pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])



# @app.callback([Output('boxes', 'style'),Output('graph', 'style'),Output('currGraph', 'style')],[Input('vbutton1', 'n_clicks'),Input('vbutton2', 'n_clicks'),Input('vbutton3', 'n_clicks')])
# def update_style(click1,click2,click3):
#    if click1==None and click2==None and click3==None:
#       return {'display': 'none'},{'display': 'none'},{'display': 'none'}
#    if(click1):
#       return {'display': 'grid'},{'display': 'none'},{'display': 'none'}
#    if(click2):
#       return {'display': 'none'},{'display': 'block'},{'display': 'none'}
#    if(click3):
#       return {'display': 'none'},{'display': 'none'},{'display': 'block'}


@app.callback(Output('boxes', 'style'),[Input('vbutton1', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'grid',
        'position': 'absolute'}


@app.callback(Output('plot', 'style'),[Input('vbutton2', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'block',
        'position': 'absolute',
        'box-shadow': '10px 5px 5px black'}

@app.callback(Output('currGraph', 'style'),[Input('vbutton3', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'block',
        'position': '',
        'float': 'right',
        'box-shadow': '10px 5px 5px black'}


# Table over opplastet data
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children=[
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


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
    result_divs=[]
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
    # i += 1
    # for o in range(i):
        # o += 1
        # return html.Div(id="currDiv" + str(o), children=[
        # html.Li(id="currLi" + str(o), children=[value]),
        # dcc.Input(id="currInput" + str(o), type="number")
        # ])


@app.callback(
    dash.dependencies.Output("currencyOutputCust", "children"),
    [dash.dependencies.Input("currencyBtnCust", "n_clicks")],
    [dash.dependencies.State("currencyChooserCust", "value")]
)
def addCurrency(n_clicks, value):
    if value:
        return html.Div(id="currDiv" + str(value), children=[
            html.Li(id="currLi" + str(value), children=[value]),
            dcc.Input(id="currInput" + str(value), type="number")
        ])
    else:
        return html.P(children="Please select your used currencies!")


# @app.callback(
    # dash.dependencies.Output("currGraph", "figure"),
    # [dash.dependencies.Input("currPercentBtn", "n_clicks"),
    # dash.dependencies.Input("currencyChooser", "value")],
    # [dash.dependencies.State("currencyInputs", "value")]
# )
# def createCurrencyGraph(n_clicks, value1, value2):
    # fig = {}
    # fig = {'data': [{'x':[i for i in value1],'y':[i for i in value2],'type':'bar','name': 'update'}]}
    # return fig
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


# Callback for Account table
@app.callback(
    dash.dependencies.Output("companyTable", "children"),
    [dash.dependencies.Input("companyBtn", "n_clicks")],
    [dash.dependencies.State("companyAccounts", "value")]
)
def createAccountTable(n_clicks, value):
    if value:
        return fetchMockData(value)
    else:
        return "Please enter number of accounts"


def fetchMockData(value):
    return createTable(value)


if __name__ == '__main__':
    app.run_server(debug=True)
