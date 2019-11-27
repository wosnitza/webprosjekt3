import dash
from dash.dependencies import Input, Output
import dash_html_components as html


external_css = [
    'https://codepen.io/muhnot/pen/RBXmaP.css'
]

app = dash.Dash(
    external_stylesheets=external_css
)

app.layout = html.Div(children=[
                      html.Button('box1', id="b1"),
                      html.Button('box2', id="b2"),
                      html.Button('box3', id="b3")
                      ])


@app.callback([Output('b1', 'style'), Output('b2', 'style'), Output('b3', 'style')], [Input('b1', 'n_clicks'), Input('b2', 'n_clicks'), Input('b3', 'n_clicks')])
def update_style(click1, click2, click3):
    if click1 == None and click2 == None and click3 == None:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    if(click1):
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    if(click2):
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    if(click3):
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
