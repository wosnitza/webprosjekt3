import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data.invoice import invoice_list
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div(id="main", children=[

    html.Div(id="lab", children=[

        html.Div(id="boxes", children=[

            html.Div(id="supplier", className="box", children=[
                html.H1(children=["Supplier stats"]),
                html.Label(id="supplierInput", children=[
                    html.P(children=["Input number of suppliers"]),
                    dcc.Input(id="supplierNr", type="number",
                              placeholder="Number of suppliers"),

                ]),

            ]),

            html.Div(id="company", className="box", children=[

            ]),

            html.Div(id="customer", className="box", children=[

            ])
        ]),
        html.Div(id="invoice-chart", children=[
            dcc.Graph(
                figure=px.bar(invoice_list,
                              x="Invoice_Date",
                              y="Amount",
                              title="Average monthly invoices",
                              ))
        ])
    ])
])


@app.callback(
    Output("invoice-chart", "children")
)
def generateInvoices():
    return [dcc.Graph(
        figure=px.bar(invoice_list,
                      x="Invoice_Date",
                      y="Amount",
                      title="Average monthly invoices",
                      ))]


if __name__ == '__main__':
    app.run_server(debug=True)
