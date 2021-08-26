import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import seaborn as sns
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://gist.githubusercontent.com/gerwolf/33c4a0de8db0687c0860967043cee39e/'
		'raw/7fdcda404cd97280b61aaf4f3337af065e238b5b/Map_Tweets_Germany.csv')

no_clusters = 17
colors = sns.color_palette(None, no_clusters).as_hex()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in list(df['Place Name'].unique())],
        value='Berlin'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)