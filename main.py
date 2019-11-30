import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from simulator_utils.invoice_generator import generate_list_of_invoices
from dash.exceptions import PreventUpdate
import dash_table
import json
import pandas as pd
import base64
import io
import plotly.graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True

app.layout = dbc.Container(
    dbc.Tabs([
        # Tab for parameters - Should update other tabs with tables and charts
        dbc.Tab(id='Tab one', label="Parameters", children=[
            dbc.Row([
                dbc.Col(id="file-upload", children=[
                    dcc.Upload(
                        id='upload',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                    )
                ])
            ]),
            dbc.Row([
                dbc.Col(id="supplier", children=[
                    html.H1("Supplier stats"),
                    dbc.Label("Monthly invoices"),
                    dbc.Input(id="invoice-monthly", className="inputs", type="number", placeholder="Monthly invoices"),
                    dbc.Label("Invoice year"),
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
                    dbc.Label("Invoices Total cost"),
                    dbc.Input(id="invoice-amount", type="number", placeholder="Invoice Total Amount"),
                    html.Div(id="currency-container", children=[
                        dbc.Label("Select Currencies"),
                        dcc.Dropdown(id="currency-selector",
                                     options=[
                                         {'label': 'Norwegian Krone — NOK', 'value': 'NOK'},
                                         {'label': 'American Dollars — USD', 'value': 'USD'},
                                         {'label': 'European Euro', 'value': 'EUR'}
                                     ]),
                        html.Div(id="currency-percentage", children=[
                        ]),
                    ]),
                    html.Label("Total procurement"),
                    dbc.Input(id="total-procurement", type="number",
                              placeholder="Select total procurement"),

                    dbc.Button("Generate", id="chart-generator"),
                ]),
                dbc.Col(id="company", children=[
                    html.H1("Company stats"),
                    dbc.Label("Accounts"),
                    dbc.Input(id="companyAccounts", type="number",
                              placeholder="Number of accounts",
                              autoFocus=False),
                    html.Div(id="companyTable", children=[

                    ]),

                    dbc.Label("Net income"),
                    dbc.Input(id="netIncomeInput", type="number",
                              placeholder="Net income"),
                    html.Div(id="netIncomeOutput", children=[

                    ]),

                    dbc.Label("Organization ID"),
                    dbc.Input(id="orgIdInput", type="number",
                              placeholder="Organization ID"),
                    html.Div(id="orgIdOutput", children=[

                    ]),
                    html.Div(id="sliderDiv"),
                ]),
                dbc.Col(id="customer", children=[
                    html.H1("Customer stats"),
                    dbc.Label("Input number of customers"),
                    dbc.Input(id="customerNr", type="number",
                              placeholder="Number of customers"),
                    html.Div(id="customerNrOutput", children=[
                    ]),
                    dbc.Label('Select your used currencies'),
                    dcc.Dropdown(id="currency-selector-customer",
                                 options=[
                                     {'label': 'Norwegian Krone — NOK', 'value': 'NOK'},
                                     {'label': 'American Dollars — USD', 'value': 'USD'},
                                     {'label': 'European Euro', 'value': 'EUR'}
                                 ]),
                    html.Div(id="currency-percentage-customer"),
                    dbc.Label("Revenue"),
                    dbc.Input(id="revenueInput", type="number",
                              placeholder="Select total revenue"),
                ])
            ])
        ]),
        # Tab for tables or charts
        dbc.Tab(id="tab-two", label='Invoice table', children=[
            dash_table.DataTable(id='table'),
        ]),
        dbc.Tab(id="tab-three", label="Accounting"),
        html.Div(id="hidden2", style={"display": "none"})
    ])
)



# Callback for currency selector
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


# Callback for invoice generator. Outputs tables in tabs
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


# Callback for upload and year slider.
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
            pnl_distribution, growth_dict = json.load(io.StringIO(decoded.decode('utf8')))
            barName = pnl_distribution.pop("Headers")

            df = pd.DataFrame(pnl_distribution)

            for key, value in df.items():
                value[1:] = value[1:] * value[0]

            df = df.T
            df.columns = barName
            df.reset_index(level=0, inplace=True, col_fill="Year")
            df.rename(columns={"index": "Year"}, inplace=True)
            # print(df)
            return [dcc.Slider(
                id="year_slider",
                min=int(df['Year'].min()),
                max=int(df['Year'].max()),
                value=int(df['Year'].min()),
                marks={str(year): str(year) for year in df['Year'].unique()},
                step=None
            ), df.to_json(date_format="iso", orient="split")]


# Callback for uploading json files with proff.no data. Creates a year slider.
@app.callback([
    dash.dependencies.Output("revenueInput", "value"),
    dash.dependencies.Output("total-procurement", "value"),
    dash.dependencies.Output("netIncomeInput", "value")
],
    [dash.dependencies.Input("year_slider", "value")],
    [dash.dependencies.State("hidden2", "children")]
)
def changeYearInfo(value, hidden_df):
    if not hidden_df:
        raise PreventUpdate
    if hidden_df:
        dff = pd.read_json(hidden_df, orient="split")
        for i in dff.index:
            if dff.loc[i, 'Year'] == value:
                print(i)
                current_revenue = dff.loc[i, "Total Revenue [NOK]"]
                current_cogs = dff.loc[i, "COGS"]
                current_netInc = dff.loc[i, "NetInc"]
                return [int(current_revenue), int(current_cogs), int(current_netInc)]


@app.callback(
    Output("tab-three", "children"),
    [Input("hidden2", "children")]
)
def createDistributionChart(hidden_df):
    if not hidden_df:
        raise PreventUpdate
    else:
        df = pd.read_json(hidden_df, orient="split")

        print(df)
        return [
            dcc.Graph(figure=go.Figure(
                data=[
                    go.Bar(
                        x=df["Year"],
                        y=df["Total Revenue [NOK]"],
                        name='Total Revenue',
                        marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                    go.Bar(
                        x=df["Year"],
                        y=df["COGS"],
                        name='Cost Of Goods Sold',
                        marker=go.bar.Marker(
                            color='rgb(26, 118, 255)'
                        )
                    ),
                    go.Bar(
                        x=df["Year"],
                        y=df["SG&A"],
                        name='Selling, General & Administrative Expense',
                        marker=go.bar.Marker(
                            color='rgb(56, 200, 155)'
                        )
                    ),
                    go.Bar(
                        x=df["Year"],
                        y=df["DA"],
                        name='Depreciation Allowance',
                        marker=go.bar.Marker(
                            color='rgb(155, 100, 50)'
                        )
                    ),
                    go.Bar(
                        x=df["Year"],
                        y=df["IntTax"],
                        name='IntTax',
                        marker=go.bar.Marker(
                            color='rgb(255, 100, 50)'
                        )
                    ),
                    go.Bar(
                        x=df["Year"],
                        y=df["NetInc"],
                        name='Net Income',
                        marker=go.bar.Marker(
                            color='rgb(135, 230, 100)'
                        )
                    )
                ],
                layout=go.Layout(
                    title='Company Accounting',
                    showlegend=True,
                    legend=go.layout.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                )
            ), id="distGraph"),
        ]

if __name__ == '__main__':
    app.run_server(debug=True)
