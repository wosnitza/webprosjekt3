import os
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from invoice import df
from dash.dependencies import Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
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
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
