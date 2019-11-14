import dash
import dash_core_components as dcc
import dash_html_components as html

print(dcc.__version__)  # 0.6.0 or above is required

external_stylesheets = [
    'style.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

])


index_page = html.Div([
    html.H1('Home'),

    dcc.Link('Go to Page 2', className='nav', href='/page-2'),
    dcc.Link('Show FX lab', className='nav', href='/page-1')

])

page_1_layout = html.Div([
    html.H1('FX LAB'),
    html.Div(id='page-1-content'),

    dcc.Link('Go to Page 2', className='nav', href='/page-2'),
    dcc.Link('Go to home', className='nav', href='/'),
])


page_2_layout = html.Div([
    html.H1('Side 2'),
    html.Div(id='page-2-content'),


    dcc.Link('Go to Page 1', className='nav', href='/page-1'),
    dcc.Link('Go to home', className='nav', href='/')
])

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
