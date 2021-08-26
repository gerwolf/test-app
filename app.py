import re
import seaborn as sns
import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
# import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

mapbox_access_token = 'pk.eyJ1IjoidGFrZWl0ZWFzeWR1ZGUiLCJhIjoiY2p5bmlrcDl4MHJ1ZTNscWs1dWp3cnAzcSJ9.b9lsNYmaCDtMpc0-HUhjow'

# df = pd.read_csv("finalrecycling.csv")

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

app = dash.Dash(__name__)

blackbold={'color':'black', 'font-weight': 'bold'}

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map
    html.Div([
       html.Div([
            # Map-legend
            # html.Ul([
            #     html.Li("Compost", className='circle', style={'background': '#ff00ff','color':'black',
            #         'list-style':'none','text-indent': '17px'}),
            #     html.Li("Electronics", className='circle', style={'background': '#0000ff','color':'black',
            #         'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            #     html.Li("Hazardous_waste", className='circle', style={'background': '#FF0000','color':'black',
            #         'list-style':'none','text-indent': '17px'}),
            #     html.Li("Plastic_bags", className='circle', style={'background': '#00ff00','color':'black',
            #         'list-style':'none','text-indent': '17px'}),
            #     html.Li("Recycling_bins", className='circle',  style={'background': '#824100','color':'black',
            #         'list-style':'none','text-indent': '17px'}),
            # ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            # ),

            # Borough_checklist
            html.Label(children=['Search word: '], style=blackbold),
            # dcc.Dropdown(id='search-word',
            #         options=[{'label': i, 'value': i} for i in ['ArminLaschet', 'Bundestagswahl', 'Deutschland']],
            #         value='', searchable = True,
            dcc.Input(id='search-word',
                    placeholder='Enter a search word...',
                    value='', type='text',
            ),

            # # Recycling_type_checklist
            # html.Label(children=['Looking to recycle: '], style=blackbold),
            # dcc.Checklist(id='recycling_type',
            #         options=[{'label':str(b),'value':b} for b in sorted(all_df['Country Code'].unique())],
            #         value=[b for b in sorted(all_df['Country Code'].unique())],
            # ),

            # Web_link
            # html.Br(),
            # html.Label(['Website:'],style=blackbold),
            # html.Pre(id='web_link', children=[],
            # style={'white-space': 'pre-wrap','word-break': 'break-all',
            #      'border': '1px solid black','text-align': 'center',
            #      'padding': '12px 12px 12px 12px', 'color':'blue',
            #      'margin-top': '3px'}
            # ),

        ], className='three columns'
        ),

        # Map

            html.Div([
            # dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
            #     style={'background':'#00FC87','padding-bottom':'2px','padding-left':'2px','height':'100vh'}
            # )
            dcc.Graph(id='graph', responsive=True)
        ], className='nine columns'
        ), 

    ], className='row'
    ),

], className='ten columns offset-by-one'
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('search-word', 'value')
              # Input('recycling_type', 'value')
              ])

def update_figure(search_word):

    # df_sub = all_df[(all_df['Place Name'].isin(chosen_boro))]

    if search_word is not None:

        row_index = []

        for i in all_df['Full Text']:

            res = i.find(search_word)

            if res != -1:

                indicator = True

            else:

                indicator = False

            row_index.append(indicator)

        df_sub = all_df[row_index]

    else:

        df_sub = all_df

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['lon'],
                    lat = df_sub['lat'],
                    mode='markers',
                    marker={'color' : df_sub['Col'], 'size' : 5},
                    text = df_sub['Place Name'] + "<br>" + "Cluster ID: "
                    # unselected={'marker' : {'opacity':1}},
                    # selected={'marker' : {'opacity':0.5, 'size':25}},
                    #hoverinfo='text',
                    #hovertext=df_sub['User Name'],
                    #customdata=df_sub['Country Code']

    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= True, #preserves state of figure/map after callback activated
            autosize = True,
            # clickmode= 'event+select',
            hovermode='closest',
            width= 700,
            height=700,
            # hoverdistance=2,
            # title=dict(text="Where to Recycle My Stuff?",font=dict(size=50, color='green')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                # style='light',
                center=dict(
                    lat=51,
                    lon=10
                ),
                pitch=0,
                zoom=3
            ),
        )
    }
#---------------------------------------------------------------
# callback for Web_link
# @app.callback(
#     Output('web_link', 'children'),
#     [Input('graph', 'clickData')])
# def display_click_data(clickData):
#     if clickData is None:
#         return 'Click on any bubble'
#     else:
#         # print (clickData)
#         the_link=clickData['points'][0]['customdata']
#         if the_link is None:
#             return 'No Website Available'
#         else:
#             return html.A(the_link, href=the_link, target="_blank")
# #--------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)