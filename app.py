import re
import os
import seaborn as sns
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

os.environ["HTTP_PROXY"] = "http://ap-python-proxy:x2o7rCPYuN1JuV8H@app-gw-2.ecb.de:8080"
os.environ["HTTPS_PROXY"] = "https://ap-python-proxy:x2o7rCPYuN1JuV8H@app-gw-2.ecb.de:8080"

mapbox_access_token = open("mapbox_token.txt").read()

df = pd.read_csv('Map_Tweets_Germany.csv')

longitude_list = []
latitude_list = []
for coord in range(len(df)):
    
    lon = re.sub("[^0-9\.]","", df['geometry'].values[coord].split(" ")[1])
    lat = re.sub("[^0-9\.]","", df['geometry'].values[coord].split(" ")[2])
    
    longitude_list.append(lon)
    latitude_list.append(lat)
    
df['lon'] = longitude_list
df['lon'] = pd.to_numeric(df['lon'])
df['lat'] = latitude_list
df['lat'] = pd.to_numeric(df['lat'])
centers_df = pd.read_csv('Centers_df.csv')
centers_longitude_list = []
centers_latitude_list = []
for coord in range(len(centers_df)):
    
    center_lon = re.sub("[^0-9\.]","", centers_df['geometry'].values[coord].split(" ")[1])
    center_lat = re.sub("[^0-9\.]","", centers_df['geometry'].values[coord].split(" ")[2])
    
    centers_longitude_list.append(center_lon)
    centers_latitude_list.append(center_lat)
    
centers_df['lon'] = centers_longitude_list
centers_df['lon'] = pd.to_numeric(centers_df['lon'])
centers_df['lat'] = centers_latitude_list
centers_df['lat'] = pd.to_numeric(centers_df['lat'])
mapbox_access_token = open("mapbox_token.txt").read()
no_clusters = 17
colors = sns.color_palette(None, no_clusters).as_hex()
col_dfs = []

traces = []

for cluster_num in set(df['Cluster Label']):
    
    sub_df = df[df['Cluster Label'] == cluster_num]
    
    sub_df['Col'] = colors[cluster_num]
    
    col_dfs.append(sub_df)

    trace = go.Scattermapbox(
    lon = sub_df['lon'],
    lat = sub_df['lat'],
    mode = 'markers',
    marker = go.scattermapbox.Marker(
    size = 5,
    color= colors[cluster_num],
    #symbol = 'star'
    ),
    text = sub_df['Place Name'] + "<br>" +
        "Cluster ID: " + str(cluster_num),
    name = 'Cluster ID:' + str(cluster_num)    
    )
    
    traces.append(trace)

cluster_center_trace = go.Scattermapbox(
    lon = centers_df['lon'],
    lat = centers_df['lat'],
    mode = 'markers',
    marker = go.scattermapbox.Marker(
    size = 7,
    color='red',
    #symbol = 'star'
    ),
    text = list(range(7)), name = 'Cluster centers'
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

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='My first web app!'),
    dcc.Graph(id='example-graph', figure=fig),
])

# @app.callback(Output('example-graph', 'figure'))

if __name__ == '__main__':
    app.run_server(debug=False)