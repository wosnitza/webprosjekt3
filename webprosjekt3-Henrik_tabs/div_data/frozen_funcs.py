# Modified version of originial showProc, that is supposed to
# help in updating graps and such.


@app.callback(
    dash.dependencies.Output("procDiv", "children"),
    [dash.dependencies.Input("procBtn", "n_clicks")],
    [dash.dependencies.State("procInput", "value")]
)
def showProc(n_clicks, value):
    if value:
        #proc_value = value
        # print(proc_value)
        return "Total procurement: {}".format(value)
    else:
        return "Please input your total procurement!"

# This callback was created in order to try to create dynamic callbacks
# it does not seem to work however, the logic is complicated


for i in curr_list:
    @app.callback(
        dash.dependencies.Output("dataStore", "data"),
        [dash.dependencies.Input("currPercentBtn", "n_clicks")],
        [dash.dependencies.State("currInput"+i, "value")]
    )
    def showCurrOfProc(n_clicks, value):
        if proc_value:
            curr_percent = value / 100
            curr_df.append({i: proc_value*curr_percent})
            return curr_df

# Another modified version of a callback, supposed to help in
# upgrading graphs and share data with other callbacks


def addCurrency(n_clicks, value):
    result_divs = []
    result_divs.append(
        html.P(children="Select how each currency influences your procurement in %"))
    if value:
        result_divs.append(html.Button(("Submit"), id="currPercentBtn"))
        for i in value:
            # curr_list.append(str(i))
            result_divs.append(html.Div(id="currDiv" + str(i), children=[
                html.Li(id="currLi" + str(i), children=[i]),
                dcc.Input(id="currInput" + str(i),
                          className="currInputs", type="number")
            ])
            )
        # print(list(curr_list))
        return result_divs
    else:
        return html.P(children="Please select your used currencies!")


# Various variables that were to be used in conjunction with callbacks
# to create functionality

curr_list = []
proc_value = 0
curr_df = pd.DataFrame()
