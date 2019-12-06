import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from simulator_utils.invoice_generator import generate_list_of_invoices
from data.mockaroo import createTable
from data.data import final_dict
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import json
import dash_table

#For upload purposes, example taken from:
#https://dash.plot.ly/dash-core-components/upload
#under upload component section
import base64
import datetime
import io


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(className="main", children=[
    html.Img(id="logo", src="/assets/logo.png"),
    html.Div(id="hidden", style={"display": "none"}),
    html.Div(id="hidden2", style={"display": "none"}),
       
    
    html.Div(id="tabDiv", children=[
        html.Button('Supplier stats', id="vbutton1"),
        html.Button('Graph 1', id="vbutton2"),
        html.Button('Graph 2', id="vbutton3"),
        html.Button('Bjornstuff', id="vbutton4"),
            html.Div(id="parameters", children=[
                html.Div(id="lab", className="main", children=[

                    html.Div(id="boxes", style={'display': 'none'}, children=[

                        html.Div(id="supplier", className="box", children=[
                            #html.Button("Submit", id="testB"),
                            html.H1(children=["Supplier stats"]),
                            html.H4(children=["Number of suppliers"]),
                            dcc.Input(id="supplierNr", type="number",
                                    placeholder="Number of suppliers",),
                            html.Button("Submit", id="supplierBtn", n_clicks=0),
                            html.Div(id="supplierNrOutput", children=[

                            ]),
                            html.H4(children="Average number of invoices per month"),
                            dcc.Input(id="avgInvoiceNr", type="number", 
                                placeholder="Number of average invoices/month"),
                            html.Button("Submit", id="invoiceBtn"),
                            html.Div(id="avgInvoicesOutput", children=[

                            ]),
                            html.H4(children=['Your used currencies']),
                            dcc.Dropdown(id="currencyChooser", options=[
                                {'label': k, 'value': v} for k, v in final_dict.items()],
                                placeholder="Select a currency..",
                                multi=True),
                            html.Button("Submit", id="currencyBtn"),
                            html.Div(id="currencyOutput", children=[
                            ]),
                            html.H4(children="Total procurement"),                      
                            html.Div(id="procDiv", children=[
                            ]),
                        ]),

                        # Company section
                        html.Div(id="company", className="box", children=[

                            html.H4(children=["Upload"]),
                             dcc.Upload(
                                id='upload',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),   
                             ),
                            html.Div(id="uploadDiv", children=[
                            ]),
                            html.Div(id="sliderDiv", children=[
                            ]),                           
                            html.H4(children=["Accounts"]),
                            dcc.Input(id="companyAccounts", type="number",
                                    placeholder="Number of accounts",
                                    autoFocus=False),
                            html.Button("Submit", id="companyBtn", n_clicks=0),
                            html.Div(id="companyTable", children=[
                            ]),
                            html.H4(children="Net income"),
                            html.Div(id="netIncomeOutput", children=[
                            ]),
                            html.H4(children="Organization ID"),
                            dcc.Input(id="orgIdInput", type="number", 
                                placeholder="Organization ID"),
                            html.Button("Submit", id="orgIdBtn"),
                            html.Div(id="orgIdOutput", children=[
                            ]),
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
                            dcc.Dropdown(id="currencyChooserCust", options=[
                                {'label': k, 'value': v} for k, v in final_dict.items()],
                                placeholder="Select a currency..",
                                searchable=True,
                                multi=True),
                            html.Button("Submit", id="currencyBtnCust"),
                            html.Div(id="currencyOutputCust", children=[
                            ]),
                            html.H4(children="Revenue"),
                            html.Div(id="revDiv", children=[

                            ]),
                        ])
                    ])
                ])
            ]),
           #Graph 1
            html.Div(id="chart1", style={'display': 'none'}, children= [
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
            ]),
            #Graph 2
            html.Div(id="chart2", style={'display': 'none'},     children=[
                html.Div(className="main", children=[
                    dcc.Graph(
                        id='diffgraph',
                        config={
                            'showSendToCloud': True,
                            'plotlyServerURL': 'https://plot.ly'
                        }
                    ),
                ])
            ]),
            html.Div(id="chart3", children=[
            html.Div(id='Tab one', children=[
        html.Div(id="parameters2", children=[
        dcc.Input(id="invoice-monthly", className="inputs", type="number", placeholder="Monthly invoices"),
        dcc.Dropdown(id="invoice-year",
                            options=[
                                {'label': '2014', 'value': '2014'},
                                {'label': '2015', 'value': '2015'},
                                {'label': '2016', 'value': '2016'},
                                {'label': '2017', 'value': '2017'},
                                {'label': '2018', 'value': '2018'}
                            ],
                            placeholder="Select Year"
                            ),
        dcc.Input(id="invoice-amount", type="number",
                        placeholder="Invoice Total Amount"),
        html.Div(id="currency-container", children=[
        html.Label("Select Currency"), dcc.Dropdown(id="currency-selector",
                                options=[
                                    {'label': 'Norwegian Krone — NOK',
                                        'value': 'NOK'},
                                    {'label': 'American Dollars — USD',
                                        'value': 'USD'},
                                    {'label': 'European Euro', 'value': 'EUR'}
                                ]),
        html.Div(id="currency-percentage", children=[
                    ]),
                ]),
        html.Button("Generate", id="chart-generator"),
            ])
        ]),
                # Tab for tables or charts
        dcc.Tab(id="tab-two", label='Tab two', children=[dash_table.DataTable(id='table'),
        ]),
        dcc.Tab(label='Tab three', children=[
        html.Div(id="test", children=[

        ])
    ]),
            ]),
        ]),
])

#Menu callbacks, one for each menu section
#Supplier Stats
@app.callback(Output('boxes', 'style'),[Input('vbutton1', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'grid',
        'position': 'absolute'}

#Graph 1 Callback
@app.callback(Output('chart1', 'style'),[Input('vbutton2', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'block',
        'position': 'absolute',
        'box-shadow': '10px 5px 5px black'}

#Graph 2 Callback
@app.callback(Output('chart2', 'style'),[Input('vbutton3', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'block',
        'position': 'relative',
        'float': 'right',
        'box-shadow': '10px 5px 5px black'}

@app.callback(Output('chart3', 'style'),[Input('vbutton4', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:    
       return {'display': 'none'}
    else:
        return {'display': 'block',
        'position': 'relative',
        'float': 'right',
        'box-shadow': '10px 5px 5px black'}

#Callback to input Org ID
#Should also get automated later?
@app.callback(
    dash.dependencies.Output("orgIdOutput", "children"),
    [dash.dependencies.Input("orgIdBtn", "n_clicks")],
    [dash.dependencies.State("orgIdInput", "value")]
)
def showAvgInvoices(n_clicks, value):
    return [
        "Your organization ID is #{}".format(
            value) if value and value > 0 else "Please input your org ID!"
    ]

#Callback to input average invoices per month
@app.callback(
    dash.dependencies.Output("avgInvoicesOutput", "children"),
    [dash.dependencies.Input("invoiceBtn", "n_clicks")],
    [dash.dependencies.State("avgInvoiceNr", "value")]
)
def showAvgInvoices(n_clicks, value):
    return [
        "You receive an average of {} invoices per month!".format(
            value) if value and value > 0 else "Please select average number of invoices received per month!"
    ]

#Callback to select number of customers
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

#Callback to select number of currencies
#And then display them
@app.callback(
    [dash.dependencies.Output("currencyOutput", "children"),
    dash.dependencies.Output("hidden", "children")],
    [dash.dependencies.Input("currencyBtn", "n_clicks")],
    [dash.dependencies.State("currencyChooser", "value")]
)
def addCurrency(n_clicks, value):
    result_divs = []
    curr_list = []
    result_divs.append(
        html.P(children="Select how each currency influences your procurement in %"))
    if value:
        #result_divs.append(html.Button(("Submit"), id="currPercentBtn"))
        curr_list.append(value)
        curr_df = pd.DataFrame(value)
        for i in range(len(value)):
            result_divs.append(html.Div(id="currDiv" + str(i), children=[
                html.Li(id="currLi" + str(i), children=["Chosen currency "+str(i)]),
                dcc.Input(id="currInput" + str(i),
                          className="currInputs", type="number")
            ])
            )
        print(curr_df)
        print(value)
        return result_divs, curr_df.to_json(date_format="iso", orient="split")
    else:
        return html.P(children="Please select your used currencies!"),html.P(children="Please select your used currencies!")
    
#Select currencies used for customers
#Then display thems
@app.callback(
    dash.dependencies.Output("currencyOutputCust", "children"),
    [dash.dependencies.Input("currencyBtnCust", "n_clicks")],
    [dash.dependencies.State("currencyChooserCust", "value")]
)
def addCurrency2(n_clicks, value):
    cust_div= []
    cust_div.append(html.P(children="Select how each currency influences your procurement in %"))
    if value:
        for i in value:
            cust_div.append(html.Div(id="currDiv" + str(i), children=[
            html.Li(id="currLi" + str(i), children=[i]),
            dcc.Input(id="currInput" + str(i), type="number")
            ])
            )
        return cust_div
    else:
        return html.P(children="Please select your used currencies!")

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

@app.callback([
    dash.dependencies.Output("sliderDiv", "children"),
    dash.dependencies.Output("hidden2", "children")],
    [dash.dependencies.Input("upload", "contents")],
    [dash.dependencies.State("upload", "filename")]
)
def uploadSlider(contents, filename):
    if contents is None:
        raise PreventUpdate
    elif contents is not None:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        if "json" in filename:
            pnl_distr, growth_dict = json.load(io.StringIO(decoded.decode('utf8')))
            barName = pnl_distr.pop('Headers')
            df = pd.DataFrame(pnl_distr)
            df = df.T
            df.columns = barName
            df.reset_index(level=0, inplace=True, col_fill="Year")
            df.rename(columns={"index": "Year"}, inplace=True)
            return [dcc.Slider(
                id="year_slider",
                min=int(df['Year'].min()),
                max=int(df['Year'].max()),
                value=int(df['Year'].min()),
                marks={str(year): str(year) for year in df['Year'].unique()},
                step=None
            ), df.to_json(date_format="iso", orient="split")]

@app.callback([
    dash.dependencies.Output("revDiv", "children"),
    dash.dependencies.Output("procDiv", "children"),
    dash.dependencies.Output("netIncomeOutput", "children")
    ],
    [dash.dependencies.Input("year_slider", "value")],
    [dash.dependencies.State("hidden2", "children")]
)

def changeYearInfo(value, hidden_df):
    if not hidden_df:
        raise PreventUpdate
    if hidden_df:
        dff = pd.read_json(hidden_df, orient="split")
        print(dff)
        stat_list = []
        for i in dff.index:
            if dff.loc[i, 'Year'] == value:
                print(i)
                current_revenue = dff.loc[i, "Total Revenue [NOK]"]
                cogs = dff.loc[i, "COGS"]
                current_cogs = current_revenue * cogs
                netInc = dff.loc[i, "NetInc"]
                current_netInc = current_revenue * netInc
                print(current_revenue)
                print(current_cogs)
                print(current_netInc)
                return [int(current_revenue), int(current_cogs), int(current_netInc)]


@app.callback(
    Output("currency-percentage", "children"),
    [Input("currency-selector", "value")],
    [State('currency-percentage', 'children')]
)
def currencyPercentage(value, existingchildren):
    if value is None:
        raise PreventUpdate
    else:
        currency = existingchildren + \
            [html.P(value), dcc.Input(
                id=str("percentage" + value), placeholder="%")]
        return currency


@app.callback(
    [Output("table", "columns"), Output("table", "data")],
    [Input("chart-generator", "n_clicks")],
    [State("invoice-monthly", "value"),
     State("invoice-year", "value"),
     State("invoice-amount", "value"),
     State("currency-percentage", "children")],
)
def createCharts(clicks, monthly, year, amount, currencylist):
    if clicks is None:
        raise PreventUpdate
    else:
        currencycodes = currencylist[::2]
        currpercentages = currencylist[1::2]

        currencycodeparsed = []
        for i, j in enumerate(currencycodes):
            currencycodeparsed.append(currencycodes[i]["props"]["children"])

        currencypercparsed = []
        for i, j in enumerate(currpercentages):
            currencypercparsed.append(
                int(currpercentages[i]["props"]["value"]))

        currency_final = dict(zip(currencycodeparsed, currencypercparsed))

        df = generate_list_of_invoices(int(year), int(
            monthly), int(amount), currency_final)
        return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')
if __name__ == '__main__':
    app.run_server(debug=True)
