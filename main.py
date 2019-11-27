import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from simulator_utils.invoice_generator import generate_list_of_invoices
from dash.exceptions import PreventUpdate
import dash_table


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([
        # Tab for parameters - Should update other tabs with tables and charts
        html.Div(id='Tab one', children=[
            html.Div(id="parameters", children=[
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
                dcc.Input(id="invoice-amount", type="number", placeholder="Invoice Total Amount"),
                html.Div(id="currency-container", children=[
                    html.Label("Select Currency"),
                    dcc.Dropdown(id="currency-selector",
                                 options=[
                                     {'label': 'Norwegian Krone — NOK', 'value': 'NOK'},
                                     {'label': 'American Dollars — USD', 'value': 'USD'},
                                     {'label': 'European Euro', 'value': 'EUR'}
                                 ]),
                    html.Div(id="currency-percentage", children=[
                    ]),
                ]),
                html.Button("Generate", id="chart-generator"),
            ])
        ]),
        # Tab for tables or charts
        dcc.Tab(id="tab-two", label='Tab two', children=[
            dash_table.DataTable(id='table'),
        ]),
        dcc.Tab(label='Tab three', children=[
            html.Div(id="test", children=[

            ])
        ]),
    ])
])


@app.callback(
    Output("currency-percentage", "children"),
    [Input("currency-selector", "value")],
    [State('currency-percentage', 'children')]
)
def currencyPercentage(value, existingchildren):
    if value is None:
        raise PreventUpdate
    else:
        currency = existingchildren + [html.P(value), dcc.Input(id=str("percentage" + value), placeholder="%")]
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
            currencypercparsed.append(int(currpercentages[i]["props"]["value"]))

        currency_final = dict(zip(currencycodeparsed, currencypercparsed))

        df = generate_list_of_invoices(int(year), int(monthly), int(amount), currency_final)
        return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
