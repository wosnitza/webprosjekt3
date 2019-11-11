import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from data import final_dict

#list_items = []

app = dash.Dash(__name__)

app.layout = html.Div(id="main", children=[
    html.Img(id="logo", src="/assets/logo.png"),

    html.Div(id="lab", children=[

        html.Div(id="boxes", children=[

            html.Div(id="supplier", className="box", children=[
                html.H1(children=["Supplier stats"]),
                html.H4(children=["Input number of suppliers"]),
                dcc.Input(id="supplierNr", type="number",
                          placeholder="Number of suppliers",
                          autoFocus=False),
                html.Button("Submit", id="supplierBtn"),
                html.Div(id="supplierNrOutput", children=[

                ]),
                html.H4(children=['Select your used currencies']),
                dcc.Dropdown(id="currencyChooser", options=[
                    {'label': k, 'value': v} for k, v in final_dict.items()],
                    placeholder="Select a currency..",
                    searchable=True),
                html.Button("Submit", id="currencyBtn"),
                html.Div(id="currencyOutput", children=[
                    html.Ul(id="currencyList", children=[
                        # html.Li(children=[item]) for item in list_items
                    ]),

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
    return "You have {} customers!".format(value)


@app.callback(
    dash.dependencies.Output("currencyList", "children"),
    [dash.dependencies.Input("currencyBtn", "n_clicks")],
    [dash.dependencies.State("currencyChooser", "value")]
)
def addCurrency(n_clicks, value):
    return html.Li(children=[value]),
    dcc.Input(className="currInput", type="number")


if __name__ == '__main__':
    app.run_server(debug=True)
