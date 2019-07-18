import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from app import app

PATH = 'Dash Data/Citations_InspectionsDataMerged_v5.csv'
mapbox_access_token = 'pk.eyJ1IjoiY29sbWVydCIsImEiOiJjanhsZWh5N3MwNWQxM25xcDB6bzNvYTU5In0.-mGdgCvd0Yy-mWhXTjJcsQ'

def load_data(PATH):
    df = pd.read_csv(PATH)
    return df

df = load_data(PATH)
YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
layout = [
    html.Div([
        html.Div([
            html.H1("Score Classification")],
            style={'textAlign': "center", "padding-bottom": "30"}),
        html.Div([html.Span("Metric to display : ", className="six columns",
                            style={"text-align": "right", "width": "40%", "padding-top": 10}),
                  html.Div([
                      dcc.Slider(
                          id='years-slider',
                          min=min(YEARS),
                          max=max(YEARS),
                          value=min(YEARS),
                          marks={str(year): str(year) for year in YEARS},
                      ),
                  ], style={'width': 400, 'margin': 25}),
        dcc.Graph(id="my-graph")
              ], className="twelve columns")
    ])
]


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("years-slider", "value")]
)
def map_maker(year):
    dff = df[df['Year'] == year]
    print(dff.head(5))
    trace = [
            go.Choropleth(
                locations=dff['Code'],
                locationmode='USA-states',
                z=dff['Score_Classification'],
                text=dff['Legal Name'],
                colorscale="YlOrRd",
            )
        ]
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        geo_scope='usa',
        showlegend=True,
        height=700,
        margin=dict(l=20, r=20, t=20, b=20),
        mapbox={
            'accesstoken': mapbox_access_token,
            'bearing': 0,
            'center': {
                'lat': 38,
                'lon': -94
            },
            'pitch': 30,
            'zoom': 3,
            'style': 'light'
        }
    )
    return {'data': trace, 'layout': layout}

