import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import re
from dash.dependencies import Input, Output

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
for cluster_num in set(df['Cluster Label']):
    
    sub_df = df[df['Cluster Label'] == cluster_num]
    
    sub_df['Col'] = colors[cluster_num]
    col_dfs.append(sub_df)
    
all_df = pd.concat(col_dfs)

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

empty_fig = go.Figure()

app = dash.Dash(__name__, external_stylesheets= external_css)

server = app.server

available_countries = all_df['Place Name'].unique()

app.layout = html.Div([
        html.Div([
            dcc.Dropdown(
                id='input-field',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Berlin', searchable = True
            ), html.Div(id='display-value'),
        ]
        ,style={'width': '30%', 'display': 'inline-block', 'horizontalAlign' : "middle", 'padding' : '1%'}),

#    ]),

dcc.Graph(id='graph', style={'height': '60vh'}),


   ])

@app.callback(
    [Output('display-value', 'children'), Output('graph', 'figure')],
    [Input('input-field', 'value')])
    # Input('disaster_selector', 'value'),
    # Input('indicator-selector', 'value'),
    #Input('indicator-graphic', 'relayoutData'),
    # Input('range-slider', 'value')])

def display_value(value):
    return 'You have selected "{}"'.format(value)

def update_graph(value):
    
    if value is not None:
    
        row_index = []
    
        for idx, i in enumerate(all_df['Full Text']):
    
            res = i.find(value)
    
            if res != -1:
            
                indicator = True
            
            else:
            
                indicator = False
            
            row_index.append(indicator)
        
        sub_df = all_df[row_index]
        
    else:
        
        sub_df = all_df
         
    locations=[go.Scattermapbox(
            
            lon = sub_df['lon'],
            lat = sub_df['lat'],
            mode = 'markers',
            marker = go.scattermapbox.Marker(size = 7, color=sub_df['Col']), # symbol = 'star'),
            text = sub_df['Place Name'] + "<br>" +
            "Cluster ID: " + str(sub_df['Cluster Label'])
            )]

    return {
        'data': locations,
        'layout': go.Layout(
            autosize=True, hovermode='closest',
            mapbox=dict(
        accesstoken=mapbox_access_token, bearing=0, center=dict(lat=51, lon=10
                                                               ), pitch=0, zoom=5
            ),)
    }
# fig = go.Figure(data = traces)
#         layout = go.Layout(
#         autosize=True,
#         hovermode='closest',
#         width = 800, 
#         height = 800,
#         mapbox=go.layout.Mapbox(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=51,
#             lon=10
#         ),
#         pitch=0,
#         zoom=5
#         ),
#         )
#         fig.layout.update(layout)

    
    # start_date = str(daterange[0]) + '-01-01'
    # end_date = str(daterange[1]) + '-01-01'
    
    # traces = []
    
    # minima = []
    # maxima = []
    
    # for i in indicator:
        
    #     minima.append(df[(df['Country'] == country_name) & (df['Year'] >= start_date) & (df['Year'] <= end_date)][i].min())
    #     maxima.append(df[(df['Country'] == country_name) & (df['Year'] >= start_date) & (df['Year'] <= end_date)][i].max())
        
    #     traces.append(go.Scatter(
        
    #     x = df[(df['Country'] == country_name) & (df['Year'] >= start_date) & (df['Year'] <= end_date)]['Year'],
    #     y = df[(df['Country'] == country_name) & (df['Year'] >= start_date) & (df['Year'] <= end_date)][i],
    #     mode = 'lines',
    #     name = str(i)
            
    #     ))
    
    # if disaster == 'Consumption disaster':
        
    #     xStart = list(cons_gantt_df[cons_gantt_df['Consumption disaster country'] == country_name]['Consumption disaster start'])
    #     xStop = list(cons_gantt_df[cons_gantt_df['Consumption disaster country'] == country_name]['Consumption disaster end'])
    #     x0 = xStart
    #     x1 = xStop
        
    #     xElem = placeholder_shape
        
    #     shp_lst = []
        
    #     for i in range(0, len(x0)):
    #         shp_lst.append(copy.deepcopy(xElem))
    #         shp_lst[i]['x0'] = x0[i]
    #         shp_lst[i]['x1'] = x1[i]
    #         shp_lst[i]['line']['color'] = 'rgba(0,0,0,0)'
            
    #     new_shape = tuple(shp_lst)
        
    # elif disaster == 'GDP disaster':
        
    #     xStart = list(gdp_gantt_df[gdp_gantt_df['GDP disaster country'] == country_name]['GDP disaster start'])
    #     xStop = list(gdp_gantt_df[gdp_gantt_df['GDP disaster country'] == country_name]['GDP disaster end'])
    #     x0 = xStart
    #     x1 = xStop
        
    #     xElem = placeholder_shape
        
    #     shp_lst = []
        
    #     for i in range(0, len(x0)):
    #         shp_lst.append(copy.deepcopy(xElem))
    #         shp_lst[i]['x0'] = x0[i]
    #         shp_lst[i]['x1'] = x1[i]
    #         shp_lst[i]['line']['color'] = 'rgba(0,0,0,0)'
            
    #     new_shape = tuple(shp_lst)
        
        
  
    # return {
        
    #     'data': traces,
    #     'layout': go.Layout(title = country_name, shapes = new_shape, xaxis = go.layout.XAxis(range = [start_date, end_date]),
    #                         uirevision = True, yaxis = go.layout.YAxis(range = [min(minima), max(maxima)], autorange = True)
    #                         ,autosize = True, showlegend = True
    #                        )
    # }


# @app.callback(Output('download-link', 'href'),
#              [Input('indicator-graphic', 'relayoutData'),
#              Input('indicator-selector', 'value'),
#              Input('country_selector', 'value'),
#              Input('range-slider', 'value')])

# def save_current_table(data_selection, indicator, country, daterange):

#     print(data_selection)

#     if data_selection == None:

#         start_date = '1871-01-01'
#         end_date= '2015-01-01'

#     elif list(data_selection.values())[0] == True:
        
#         start_date = str(daterange[0]) + '-01-01'
#         end_date= str(daterange[1]) + '-01-01'

#     else:

#         start_date = list(data_selection.values())[0][0]
#         end_date = list(data_selection.values())[0][1]

#     indicator.append('Year')
#     indicator.append('Country')

#     final_df = df[(df['Year'] >= start_date) & (df['Year'] <= end_date) & (df['Country'] == country)][indicator]

#     csv_string = final_df.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(csv_string)

#     return csv_string


# @app.callback(Output('download-link-full', 'href'),
#             [Input('range-slider', 'value')])

# def save_full_dataset(daterange):

#     print(daterange, len(df))

#     csv_string_full = df.to_csv(index = False, encoding = 'utf-8')
#     csv_string_full = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(csv_string_full)

#     return csv_string_full

if __name__ == '__main__':
    app.server.run(debug=True)