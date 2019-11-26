import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from data.mockaroo import createTable
from data.data import final_dict
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import json

#For upload purposes, example taken from:
#https://dash.plot.ly/dash-core-components/upload
#under upload component section
import base64
import datetime
import io


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

curr_list = []
#proc_value = 0
#curr_df = pd.DataFrame()

app.layout = html.Div(className="main", children=[
    html.Img(id="logo", src="/assets/logo.png"),
    html.Button("Test", id="testButton"),
    html.Div(id="hidden", style={"display": "none"}),
    html.Div(id="hidden2", style={"display": "none"}),

    html.Div(id="tabDiv", children=[
            html.Div(id="parameters", children=[
                html.Div(id="lab", className="main", children=[

                    html.Div(id="boxes", children=[

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
                                # html.Ul(id="currencyList", children=[
                                # html.Li(children=[item]) for item in list_items
                                # ]),
                            ]),
                            html.H4(children="Total procurement"),
                            dcc.Input(id="procInput", type="number",
                                    placeholder="Select total procurement"),
                            html.Button("Submit", id="procBtn"),
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
                                style={
                                    'width': '80%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
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
                            dcc.Input(id="netIncomeInput", type="number", 
                                placeholder="Net income"),
                            html.Button("Submit", id="netIncomeBtn"),
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
                                # html.Ul(id="currencyList", children=[
                                # html.Li(children=[item]) for item in list_items
                                # ]),

                            ]),
                            html.H4(children="Revenue"),
                            dcc.Input(id="revInput", type="number",
                                    placeholder="Select total revenue"),
                            html.Button("Submit", id="revBtn"),
                            html.Div(id="revDiv", children=[

                            ]),
                        ])
                    ])
                ])

            ]),
            html.Hr(),

            html.Div(id="chart1", children= [
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
            html.Hr(),

            html.Div(id="chart2", children=[
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
                        id='diffgraph',
                        config={
                            'showSendToCloud': True,
                            'plotlyServerURL': 'https://plot.ly'
                        }
                    ),
                ])
            ]),

            html.Div(id="chart3", children=[

            ]),
        ]),
])
    #html.Div(id="appLayout")

#@app.callback(
    #dash.dependencies.Output("currGraph", "figure"),
    #[dash.dependencies.Input("testB", "n_clicks")],
    #[dash.dependencies.State("hidden", "children")],
    #[dash.dependencies.State("procDiv", "children")],
    #[dash.dependencies.State("currInput{i}", "value") for i in range(0,5)],
    #[dash.dependencies.State("currInput{i}", "value") for i in range(0,5)],
    #[dash.dependencies.State("currInput{i}", "value") for i in range(0,5)],
    #[dash.dependencies.State("currInput{i}", "value") for i in range(0,5)],
    #[dash.dependencies.State("currInput{i}", "value") for i in range(0,5)],
#)
#def test(n_clicks, json_data, procurement, value1, value2, value3, value4, value5):
    #read_df = pd.read_json((json_data))
    #new_df = pd.DataFrame(columns=[])
    #for row in read_df.iterrows():


    #fig={
        #'data': [
                    #{'x': [for row in read_df.iterrows()], 'y': curr_dict.values(),
                    #'type': 'bar', 'name': 'SF'},
                #],
        #'layout': {
                #'title': 'Test'
            #}
    #}
    #return fig

#Callback to input net income
#Should get automated after a while
#@app.callback(
    #dash.dependencies.Output("netIncomeOutput", "children"),
    #[dash.dependencies.Input("netIncomeBtn", "n_clicks")],
    #[dash.dependencies.State("netIncomeInput", "value")]
#)
#def showAvgInvoices(n_clicks, value):
    #return [
        #"You have a net income of {}".format(
            #value) if value and value > 0 else "Please input your net income!"
    #]

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
    #i += 1
    # for o in range(i):
        #o += 1
        # return html.Div(id="currDiv" + str(o), children=[
        #html.Li(id="currLi" + str(o), children=[value]),
        #dcc.Input(id="currInput" + str(o), type="number")
        # ])


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


# @app.callback(
    #dash.dependencies.Output("currGraph", "figure"),
    # [dash.dependencies.Input("currPercentBtn", "n_clicks"),
    # dash.dependencies.Input("currencyChooser", "value")],
    #[dash.dependencies.State("currencyInputs", "value")]
# )
# def createCurrencyGraph(n_clicks, value1, value2):
    #fig = {}
    #fig = {'data': [{'x':[i for i in value1],'y':[i for i in value2],'type':'bar','name': 'update'}]}
    # return fig
# for i in stats_layout['currencyOutput'].children

#Callback for inputting total procureement
#To be changed later
#@app.callback(
    #dash.dependencies.Output("procDiv", "children"),
    #[dash.dependencies.Input("procBtn", "n_clicks")],
    #[dash.dependencies.State("procInput", "value")]
#)
#def showProc(n_clicks, value):
    #if value:
        #return "Total procurement: {}".format(value)
    #else:
        #return "Please input your total procurement!"

#Callback to input and display revenue
#@app.callback(
    #dash.dependencies.Output("revDiv", "children"),
    #[dash.dependencies.Input("revBtn", "n_clicks")],
    #[dash.dependencies.State("revInput", "value")]
#)
#def showProc(n_clicks, value):
    #if value:
        #return "Your revenue: {}".format(value)
    #else:
        #return "Please input your revenue!"


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

#Original callback for file upload, converting the json to a dataframe
#and then updating several elements in the layout 
#with information taken from the dataframe
#@app.callback([
    #dash.dependencies.Output("uploadDiv", "children"),
    #dash.dependencies.Output("revDiv", "children"),
    #dash.dependencies.Output("procDiv", "children"),
    #dash.dependencies.Output("netIncomeOutput", "children")
    #],
    #[dash.dependencies.Input("upload", "contents")],
    #[dash.dependencies.State("upload", "filename")]

#)
#def uploadParse(contents, filename):
    #if contents is None:
        #raise PreventUpdate
    #elif contents is not None:
        #content_type, content_string = contents.split(',')

        #decoded = base64.b64decode(content_string)
        #if contents is not None:
            #if 'csv' in filename:
                #df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                #print(df)
                #df.set_index("Year")
                #Commenting this one, gives COGS keyerror
                #df.columns = df.columns.str.strip()
                #This one gives AttributeError: 'Index' object has no attribute 'lower'
                #df.columns = df.columns.str.strip().lower()
                #Commenting this one, gives total revenue nok KeyError
                #df.columns = df.columns.str.lower()
                #success_msg = html.P("File upload was succesful!")
                #current_revenue = df.loc["year","Total Revenue [NOK]"]
                #cogs = df.loc["year","COGS"]
                #current_cogs = current_revenue * cogs
                #netInc = df.loc["year","NetInc"]
                #current_netInc = current_revenue * netInc
                #current_revenue = df.ix[4, "Total Revenue [NOK]"]
                #current_cogs = current_revenue * df.ix[4, "COGS"]
                #current_netInc = current_revenue * df.ix[4, "NetInc"]
                #return [success_msg, current_revenue, current_cogs, current_netInc]
            #elif "json" in filename:
                #df = pd.read_json(io.StringIO(decoded.decode('utf-8')))
                #pnl_distr, growth_dict = json.load(io.StringIO(decoded.decode('utf8')))
                #barName = pnl_distr.pop('Headers')
                #df = pd.DataFrame(pnl_distr)
                #print(df)
                #df = df.T
                #df.columns = barName
                #df.reset_index(level=0, inplace=True, col_fill="Year")
                #df.rename(columns={"index": "Year"}, inplace=True)
                #print(df)
                #print(df["Total Revenue [NOK]"])

                #success_msg = html.P("File upload was succesful!")
                #current_revenue = df.loc[4, "Total Revenue [NOK]"]
                #current_revenue = df['Total Revenue [NOK]'].iloc[-1]
                #cogs = df.loc[4,"COGS"]
                #cogs = df['COGS'].iloc[-1]
                #current_cogs = current_revenue * cogs
                #netInc = df.loc[4, "NetInc"]
                #netInc = df['NetInc'].iloc[-1]
                #current_netInc = current_revenue * netInc

                #return [success_msg, current_revenue, current_cogs, current_netInc]
    

            #else:
                #error_msg = "File must be of type .json!"
                #filler = "Something"
                #filler2 = "Something else"
                #filler3 = "Something more"
                #return [error_msg, error_msg, error_msg, error_msg]
                #return [1,2,3,4]


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
            #print(df)
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
    #hidden_info = json.loads(hidden_df)
    #new_df = pd.DataFrame(hidden_info)
    dff = pd.read_json(hidden_df, orient="split")
    print(dff)
    stat_list = []
    for i, c in dff.iterrows():
        if i == value:
            print(i)
            #success_msg = html.P("File upload was succesful!")
            #current_revenue = dff.loc[4, "Total Revenue [NOK]"]
            #current_revenue = dff.loc[str(i), "Total Revenue [NOK]"]
            current_revenue = dff.loc[i, c["Total Revenue [NOK]"]]
            #current_revenue = dff['Total Revenue [NOK]'].iloc[i]
            #cogs = dff.loc[4,"COGS"]
            #cogs = dff['COGS'].iloc[i]
            cogs = dff.loc[str(i), "COGS"]
            current_cogs = current_revenue * cogs
            #netInc = dff.loc[4, "NetInc"]
            #netInc = dff['NetInc'].iloc[i]
            netInc = dff.loc[str(i), "NetInc"]
            current_netInc = current_revenue * netInc
            print(current_revenue)
            print(current_cogs)
            print(current_netInc)
            return [current_revenue, current_cogs, current_netInc]
            #stat_list.append(current_revenue, current_cogs, current_netInc)

    #return stat_list

#Below is the upload file callback function
#But it is designed for use with JSON
            #if 'json' in content_type and 'json' in filename:
                #json_loaded = json.load(decoded)
                #df = pd.read_json(json_loaded, orient="index")
                #success_msg = html.P("File upload was succesful!")
                #current_revenue = df[:-1][1]
                #current_cogs = current_revenue * df[:-1][2]
                #current_netInc = current_revenue * df[:-1][7]
                #return html.P("File upload was succesful!"), current_revenue, current_cogs, current_netInc
                #return [success_msg, current_revenue, current_cogs, current_netInc]
                #return [1,2,3,4]
            #else:
                #error_msg = "File must be of type .json!"
                #filler = "Something"
                #filler2 = "Something else"
                #filler3 = "Something more"
                #return [error_msg, error_msg, error_msg, error_msg]
                #return [1,2,3,4]

# @app.callback(
    #dash.dependencies.Output("infoDiv", "children"),
    #[dash.dependencies.Input("supplierBtn", "n_clicks")],
    #[dash.dependencies.State("supplierNr", "value")]
# )
# def showTest(n_clicks, value):
    # return "test"

#@app.callback(
    #dash.dependencies.Output("infoDiv", "children"),
    #[dash.dependencies.Input("currencyBtnCust", "n_clicks")],
    #[dash.dependencies.State("currencyChooserCust", "value")]
#)
#def addCurrency_2(n_clicks, value):
    #if value:
        #return html.Div(id="currDiv" + str(value), children=[
            #html.Li(id="currLi" + str(value), children=[value]),
            #dcc.Input(id="currInput" + str(value), type="number")
        #])
    #else:
        #return html.P(children="Please select your used currencies!")


#@app.callback(
    #dash.dependencies.Output("testDiv", "children"),
    #[dash.dependencies.Input("testBtn", "n_clicks")],
    #[dash.dependencies.State("infoDiv", "children")]
#)
#def showTest2(n_clicks, value):
    #return value


if __name__ == '__main__':
    app.run_server(debug=True)
