import dash
import dash_core_components as dcc
import dash_html_components as html
from data.data import final_dict
from data.mockaroo import table
import pandas as pd
# list_items = []
i = 0

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
                html.Button("Submit", id="supplierBtn", n_clicks=0),
                html.Div(id="supplierNrOutput", children=[

                ]),
                html.H4(children=['Select your used currencies']),
                dcc.Dropdown(id="currencyChooser", options=[
                    {'label': k, 'value': v} for k, v in final_dict.items()],
                             placeholder="Select a currency..",
                             searchable=True),
                html.Button("Submit", id="currencyBtn"),
                html.Div(id="currencyOutput", children=[
                    # html.Ul(id="currencyList", children=[
                    # html.Li(children=[item]) for item in list_items
                    # ]),
                ]),
            ]),


            # Company section
            html.Div(id="company", className="box", children=[
                table
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
    dash.dependencies.Output("company", "children")
)
def addCompany():
    return generateTable()

@app.callback(
    dash.dependencies.Output("currencyOutput", "children"),
    [dash.dependencies.Input("currencyBtn", "n_clicks")],
    [dash.dependencies.State("currencyChooser", "value")]
)
def addCurrency(n_clicks, value):
    if value:
        return html.Div(id="currDiv" + str(value), children=[
            html.Li(id="currLi" + str(value), children=[value]),
            dcc.Input(id="currInput" + str(value), type="number")
        ])
    else:
        return html.P(children="Please select your used currencies!")


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



if __name__ == '__main__':
    app.run_server(debug=True)
