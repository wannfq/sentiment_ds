import os
import dash
from nlp_module import *
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#aaaabb',
    'header': '#121244',
    'subtext': '#444466',
}

app.layout = html.Div([
    html.Div([
        html.H1(
            children='Movie Review Analyzer',
            style={
                'text-align': 'center',
                'color': colors['header'],
                'margin-top': '2em',
            }),
    ], className='app-header'),
    html.Hr(),
    dcc.Textarea(
        id='review-textarea',
        value='',
        placeholder='Type your review about the movie',
        style={
            'width': '100%',
            'margin-bottom': '1em',
        }
    ),
    html.Button('Classify', id='detect-button', n_clicks=0),
    html.Hr(),
    html.Div(id='display-value')
])

@app.callback(
    dash.dependencies.Output('display-value', 'children'),
    [dash.dependencies.Input(component_id='detect-button', component_property='n_clicks')],
    [dash.dependencies.State(component_id='review-textarea', component_property='value')]
)

def display_value(n_clicks, value):
    if value == '':
        raise PreventUpdate
    else:
        return 'This is likely a "{}" review'.format(guess_sentiment(value))

if __name__ == '__main__':
    app.run_server(debug=True)
