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
import calculate_exposure as ce

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True

app.layout = dbc.Container(children=[
    html.Img(className="logo", src="assets/5.png"),
    dbc.Tabs([
        # Tab for parameters - Should update other tabs with tables and charts
        dbc.Tab(id='Tab one', label="Parameters", labelClassName="menu", children=[
            dbc.Row([
                dbc.Col(id="file-upload", children=[
                    html.Img(className="dragdrop", src="assets/dragdrop.png"),
                    dcc.Upload(
                        id='upload',
                        children=html.Div([
                            html.A('Drag and drop'),
                            html.P('or select files')
                        ]),
                    )
                ])
            ]),
            dbc.Row([
                dbc.Col(id="supplier", children=[
                    html.H1("Supplier stats"),
                    dbc.Label("Yearly Invoices"),
                    dbc.Input(id="invoice-yearly-supplier", className="inputs", type="number",
                              placeholder="Invoices per. year"),
                    dbc.Label("Invoice year"),
                    dcc.Dropdown(id="invoice-year-supplier",
                                 options=[
                                     {'label': '2014', 'value': '2014'},
                                     {'label': '2015', 'value': '2015'},
                                     {'label': '2016', 'value': '2016'},
                                     {'label': '2017', 'value': '2017'},
                                     {'label': '2018', 'value': '2018'}
                                 ],
                                 placeholder="Select Year"
                                 ),
                    dbc.Label("Total procurement"),
                    dbc.Input(id="total-procurement", type="number",
                              placeholder="Select total procurement"),
                    html.Div(id="currency-container-supplier", children=[
                        dbc.Label("Currency distribution"),
                        dcc.Dropdown(id="currency-selector-supplier",
                                     options=[
                                         {'label': 'Norwegian Krone — NOK',
                                             'value': 'NOK'},
                                         {'label': 'American Dollars — USD',
                                             'value': 'USD'},
                                         {'label': 'European Euro', 'value': 'EUR'}
                                     ]),
                        html.Div(id="currency-percentage-supplier", children=[
                        ]),
                    ]),
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
                    dbc.Label("Yearly Invoices"),
                    dbc.Input(id="invoice-monthly-customer", type="number",
                              placeholder="Invoices per year"),
                    dbc.Label("Invoice year"),
                    dcc.Dropdown(id="invoice-year-customer",
                                 options=[
                                     {'label': '2014', 'value': '2014'},
                                     {'label': '2015', 'value': '2015'},
                                     {'label': '2016', 'value': '2016'},
                                     {'label': '2017', 'value': '2017'},
                                     {'label': '2018', 'value': '2018'}
                                 ],
                                 placeholder="Select Year"
                                 ),
                    dbc.Label("Total Revenue"),
                    dbc.Input(id="total-revenue", type="number",
                              placeholder="Select total revenue"),
                    dbc.Label("Currency distribution"),
                    dcc.Dropdown(id="currency-selector-customer",
                                 options=[
                                     {'label': 'Norwegian Krone — NOK',
                                         'value': 'NOK'},
                                     {'label': 'American Dollars — USD',
                                         'value': 'USD'},
                                     {'label': 'European Euro', 'value': 'EUR'}
                                 ]),
                    html.Div(id="currency-percentage-customer", children=[
                    ]),

                ])
            ])
        ]),
        # Tab for tables or charts
        # dbc.Tab(id="tab-two", label='Invoice Suppliers', children=[
        #     dash_table.DataTable(id='table-supplier'),
        # ]),
        # dbc.Tab(id="tab-three", label='Invoice Customers', children=[
        #     dash_table.DataTable(id='table-customer'),
        # ]),
        dbc.Tab(id="tab-four", label="Accounting", labelClassName="menu"),
        dbc.Tab(id='tab-five', label="Exposure", labelClassName="menu", children=[
            html.H1("Exposure chart"),
            dbc.Row([
                dbc.Col(id="exposure-data", width=4, children=[
                    dcc.Dropdown(id="exposure-year", placeholder="Year"),
                    dcc.Dropdown(id="exposure-type",
                                 placeholder="Exposure Type"),
                    html.Div(id="exposure-overview")
                ]),
                dbc.Col(id="exposure", children=[
                    dcc.Graph(id="exposure-chart"),
                    dash_table.DataTable(id='exposure-table'),
                ])
            ]),
            dbc.Button("Generate exposure", id="generate"),
        ]),
        # Hidden divs for storing data from callbacks
        html.Div(id="hidden2", style={"display": "none"}),
        html.Div(id="hidden-df-exposure", style={"display": "none"}),
        html.Div(id="hidden-div-company", style={"display": "none"}),
    ])
])


"""Test code for set up company"""


@app.callback(
    Output("hidden-div-company", "children"),
    [Input("chart-generator", "n_clicks")],
    [State("invoice-yearly-supplier", "value"),
     State("invoice-year-supplier", "value"),
     State("netIncomeInput", "value"),
     State("total-revenue", "value"),
     State("currency-percentage-supplier", "children"),
     State("currency-percentage-customer", "children")],
)
def createCharts(clicks, yearly_invoices, year, net_inc, total_revenue, currency_supplier, currency_customer):
    if clicks is None:
        raise PreventUpdate
    else:
        # Code for processing currency distribution on supplier side
        currency_codes_supplier=currency_supplier[::2]
        currency_percentages_supplier=currency_supplier[1::2]
        currency_code_supplier_list=[]
        for i, j in enumerate(currency_codes_supplier):
            currency_code_supplier_list.append(
                currency_codes_supplier[i]["props"]["children"])
        currency_percentage_supplier_list=[]
        for i, j in enumerate(currency_percentages_supplier):
            currency_percentage_supplier_list.append(
                int(currency_percentages_supplier[i]["props"]["value"]))
        currency_dist_supplier=dict(
            zip(currency_code_supplier_list, currency_percentage_supplier_list))

        # Code for processing currency distribution on customer side
        currency_codes_customer = currency_customer[::2]
        currency_percentages_customer = currency_customer[1::2]
        currency_code_customer_list = []
        for i, j in enumerate(currency_codes_customer):
            currency_code_customer_list.append(
                currency_codes_customer[i]["props"]["children"])
        currency_percentages_customer_list = []
        for i, j in enumerate(currency_percentages_customer):
            currency_percentages_customer_list.append(
                int(currency_percentages_customer[i]["props"]["value"]))
        currency_dist_customer = dict(
            zip(currency_code_customer_list, currency_percentages_customer_list))

        company = {str(year): {'Total_Revenue': int(total_revenue),
                               'Net_Income': int(net_inc),
                               'Amount_of_Invoices': int(yearly_invoices),
                               'Proc_Currency_Distribution': currency_dist_supplier,
                               'Sales_Currency_Distribution': currency_dist_customer}
                   }
        company, sales, procurement, net_income = ce.cc.set_up_company(company)
        pnl_distribution, yoy_growth_dict, distribution_dict = \
            ce.generate_mock_company(company, sales, procurement, net_income)

        pnl_distribution, yoy_growth_dict, distribution_dict, currencies, currency_risks, account_factor_vector = \
            ce.load_pnl_and_currency_data(
                pnl_distribution, yoy_growth_dict, distribution_dict)

        exposure_df = ce.clean_up_and_sort_results(ce.construct_exposure_matrix(pnl_distribution,
                                                                                yoy_growth_dict,
                                                                                distribution_dict,
                                                                                currencies,
                                                                                currency_risks,
                                                                                account_factor_vector))

        exposure_df = exposure_df.to_json(date_format="iso", orient="split")

        return exposure_df


"""Test code for set up company"""


# Callback for currency selector supplier side
@app.callback(
    Output("currency-percentage-supplier", "children"),
    [Input("currency-selector-supplier", "value")],
    [State('currency-percentage-supplier', 'children')]
)
def currencyPercentageSupplier(value, existingchildren):
    if value is None:
        raise PreventUpdate
    else:
        currency = existingchildren + \
            [html.P(value), dbc.Input(
                id=str("percentage" + value), placeholder="%")]
        return currency


# Callback for currency selector customer side
@app.callback(
    Output("currency-percentage-customer", "children"),
    [Input("currency-selector-customer", "value")],
    [State('currency-percentage-customer', 'children')]
)
def currencyPercentageSupplier(value, existingchildren):
    if value is None:
        raise PreventUpdate
    else:
        currency = existingchildren + \
            [html.P(value), dbc.Input(
                id=str("percentage" + value), placeholder="%")]
        return currency


# Callback for invoice generator. Outputs tables in tabs
# @app.callback(
#     [Output("table-supplier", "columns"), Output("table-supplier", "data")],
#     [Input("chart-generator", "n_clicks")],
#     [State("invoice-monthly-supplier", "value"),
#      State("invoice-year-supplier", "value"),
#      State("total-procurement", "value"),
#      State("currency-percentage-supplier", "children")],
# )
# def createCharts(clicks, monthly, year, amount, currencylist):
#     if clicks is None:
#         raise PreventUpdate
#     else:
#         currencycodes = currencylist[::2]
#         currpercentages = currencylist[1::2]
#
#         currencycodeparsed = []
#         for i, j in enumerate(currencycodes):
#             currencycodeparsed.append(currencycodes[i]["props"]["children"])
#
#         currencypercparsed = []
#         for i, j in enumerate(currpercentages):
#             currencypercparsed.append(int(currpercentages[i]["props"]["value"]))
#
#         currency_final = dict(zip(currencycodeparsed, currencypercparsed))
#
#         df = generate_list_of_invoices(int(year), int(monthly), int(amount), currency_final, "COGS")
#         return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')


# Callback for invoice generator customer side. Outputs tables in tabs
# @app.callback(
#     [Output("table-customer", "columns"), Output("table-customer", "data")],
#     [Input("chart-generator", "n_clicks")],
#     [State("invoice-monthly-customer", "value"),
#      State("invoice-year-customer", "value"),
#      State("total-revenue", "value"),
#      State("currency-percentage-customer", "children")],
# )
# def createCharts(clicks, monthly, year, amount, currencylist):
#     if clicks is None:
#         raise PreventUpdate
#     else:
#         currencycodes = currencylist[::2]
#         currpercentages = currencylist[1::2]
#
#         currencycodeparsed = []
#         for i, j in enumerate(currencycodes):
#             currencycodeparsed.append(currencycodes[i]["props"]["children"])
#
#         currencypercparsed = []
#         for i, j in enumerate(currpercentages):
#             currencypercparsed.append(int(currpercentages[i]["props"]["value"]))
#
#         currency_final = dict(zip(currencycodeparsed, currencypercparsed))
#
#         df = generate_list_of_invoices(int(year), int(monthly), int(amount), currency_final, "Revenue")
#         return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')


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
            pnl_distribution, growth_dict = json.load(
                io.StringIO(decoded.decode('utf8')))
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


# Callback for uploading json files with proff.no data. Updates inputs from slider
@app.callback([
    Output("total-revenue", "value"),
    Output("total-procurement", "value"),
    Output("netIncomeInput", "value"),
    Output("invoice-year-supplier", "value"),
    Output("invoice-year-customer", "value")
],
    [Input("year_slider", "value")],
    [State("hidden2", "children")]
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
                current_year = dff.loc[i, "Year"]
                return [int(current_revenue), int(current_cogs), int(current_netInc), int(current_year),
                        int(current_year)]


# Callback for creating distribution barchart from pnl-distribution json
@app.callback(
    Output("tab-four", "children"),
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


"""Start of callbacks for exposure engine"""


# @app.callback(
#     Output("hidden-df-exposure", "children"),
#     [Input("generate", "n_clicks")]
# )
# def storeExposureData(click):
#     if click is None:
#         raise PreventUpdate
#     else:
#         df = ce.main()
#         df = df.sort_values(by="Year")
#         return df.to_json(date_format="iso", orient="split")


@app.callback(
    Output("exposure-overview", "children"),
    [
        Input("exposure-type", "value"),
        Input("exposure-year", "value")],
    [State("hidden-div-company", "children")]
)
def exposureOverview(exposure_type, exposure_year, hidden_df):
    if not hidden_df:
        raise PreventUpdate
    else:
        df = pd.read_json(hidden_df, orient="split")
        dfyear = df["Year"] == exposure_year
        dftype = df["Type_of_Exposure"] == exposure_type
        df_overview = df[dfyear & dftype]
        df_overview = df_overview.round(0)
        df_overview = df_overview.sort_values(
            by="Exposed_Amount_(Risked)", ascending=False)
        df_overview.loc["Exposed_Amount_(Risked)"] = df_overview.sum()
        df_overview["Currency"].iloc[-1] = "Grand Total"

        table = dbc.Table.from_dataframe(df_overview, striped=True, bordered=True, hover=True,
                                         size="sm",
                                         responsive="sm",
                                         columns=["Currency",
                                                  "Exposed_Amount_(Risked)"],
                                         header=["Currencies", "Sum of Exposed Amount (Risked)"])
        return table


# Callback for populating exposure dropdown menus
@app.callback(
    [Output("exposure-year", "options"),
     Output("exposure-year", "value"),
     Output("exposure-type", "options"),
     Output("exposure-type", "value")],
    [Input("hidden-div-company", "children")]
)
def exposureDropdowns(hidden_df):
    if not hidden_df:
        raise PreventUpdate
    else:
        df = pd.read_json(hidden_df, orient="split")
        return ([{"label": i, "value": i} for i in df.Year.unique()]), df["Year"].iloc[-1], \
               ([{"label": i, "value": i}
                 for i in df.Type_of_Exposure.unique()]), df["Type_of_Exposure"][0],


# Callback for creating exposure bar-chart
@app.callback(
    Output("exposure-chart", "figure"),
    [
        Input("exposure-type", "value"),
        Input("exposure-year", "value")],
    [State("hidden-div-company", "children")]
)
def exposureChart(exposure_type, exposure_year, hidden_df):
    if not hidden_df:
        raise PreventUpdate
    else:
        df = pd.read_json(hidden_df, orient="split")
        dfyear = df["Year"] == exposure_year
        dftype = df["Type_of_Exposure"] == exposure_type
        df_dynamic = df[dfyear & dftype]
        df_dynamic = df_dynamic.sort_values(by="Currency", ascending=True)
        return go.Figure(
            data=[
                go.Bar(
                    x=df_dynamic["Currency"],
                    y=df_dynamic["Exposed_Amount_(Risked)"],
                    name='Total Revenue',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                )
            ])


# Callback for creating table of exposure dataframe
# @app.callback(
#     [Output("exposure-table", "columns"), Output("exposure-table", "data")],
#     [Input("generate", "n_clicks")]
# )
# def exposureGenerator(clicks):
#     if clicks is None:
#         raise PreventUpdate
#     else:
#         df_exposure = calculate_exposure.main()
#         return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')


"""End of callbacks for exposure engine"""

if __name__ == '__main__':
    app.run_server(debug=True)
