import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from data.data import final_dict

parameters_layout = [
    html.Div(id="lab", className="main", children=[

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
                          placeholder="Number of customers",
                          autoFocus=False),
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
    ])
]
