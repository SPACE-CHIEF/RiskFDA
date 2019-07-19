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
            html.H1("Risk Score Classification")],
            style={'text-align': "center", "padding-bottom": "30"}),
        html.Div([
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
    dt = dff['Legal Name'] + '<br>' + 'Classification: ' + dff['Classification']
    trace = [
        go.Choropleth(
            locations=dff['Code'],
            locationmode='USA-states',
            z=dff['Score_Classification'],
            text=dt,
            colorscale="Portland",
            geo = 'geo2'
        )
    ]
    layout = go.Layout(
        geo2 = dict(
            scope = 'usa',
            #projection=dict(type='natural earth'),
            projection=go.layout.geo.Projection(type='albers usa')
        )
    )
    return {'data': trace, 'layout': layout}

