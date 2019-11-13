import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from data.mockaroo import createTable
from data.data import final_dict
from tabs import parameters, chart1, chart2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div(className="main", children=[
    html.Img(id="logo", src="/assets/logo.png"),

    html.Div(id="infoDiv", style={"display": "none"}),

    dcc.Tabs(id="mainTab", value="stats_tab", children=[
        dcc.Tab(label="Parameters", value="parameters_tab"),
        dcc.Tab(label="Chart 1", value="chart1_tab"),
        dcc.Tab(label="Chart 2", value="chart2_tab")
    ]),

    html.Div(id="appLayout")
])


@app.callback(
    dash.dependencies.Output("appLayout", "children"),
    [dash.dependencies.Input("mainTab", "value")]
)
def render_layout(tab):
    if tab == "parameters_tab":
        return parameters.parameters_layout
    elif tab == "chart1_tab":
        return chart1.chart1_layout
    elif tab == "chart2_tab":
        return chart2.chart2_layout


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
    result_divs = []
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
    #i += 1
    # for o in range(i):
        #o += 1
        # return html.Div(id="currDiv" + str(o), children=[
        #html.Li(id="currLi" + str(o), children=[value]),
        #dcc.Input(id="currInput" + str(o), type="number")
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
