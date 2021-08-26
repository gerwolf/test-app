import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import seaborn as sns
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://gist.githubusercontent.com/gerwolf/33c4a0de8db0687c0860967043cee39e/'
		'raw/7fdcda404cd97280b61aaf4f3337af065e238b5b/Map_Tweets_Germany.csv')

centers_df = pd.read_csv('https://gist.githubusercontent.com/gerwolf/2455b1208428f0715e63aded28cfcd55/'
		'raw/1d8d088bcbfc97b1376d67fd94cff669a5daa62a/Centers_df.csv')

mapbox_access_token = open("mapbox_token.txt").read()

no_clusters = 17
colors = sns.color_palette(None, no_clusters).as_hex()

traces = []

for cluster_num in set(cluster_labels):
    
    sub_df = df[df['Cluster Label'] == cluster_num]
    
    trace = go.Scattermapbox(
    lon = sub_df['geometry'].values.x,
    lat = sub_df['geometry'].values.y,
    mode = 'markers',
    marker = go.scattermapbox.Marker(
    size = 5,
    color= colors[cluster_num],
    #symbol = 'star'
    ),
    text = sub_df['Place Name'] + "<br>" +
        "Cluster ID: " + str(cluster_num)
    )
    
    traces.append(trace)
    
cluster_center_trace = go.Scattermapbox(
    lon = centers_df['geometry'].values.x,
    lat = centers_df['geometry'].values.y,
    mode = 'markers',
    marker = go.scattermapbox.Marker(
    size = 7,
    color='red',
    #symbol = 'star'
    ),
    text = list(range(no_clusters))
    )

traces.append(cluster_center_trace)
    
fig = go.Figure(data = traces)

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    width = 800, 
    height = 800,
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=51,
            lon=10
        ),
        pitch=0,
        zoom=5
    ),
)

fig.layout.update(layout)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in list(df['Place Name'].unique())],
        value='Berlin'
    ),
    html.Div(id='display-value'),

	dcc.Graph(id='Tweets-Map', figure=fig)
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)