import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import us
from app import app

mapbox_access_token = 'pk.eyJ1IjoiY29sbWVydCIsImEiOiJjanhsZWh5N3MwNWQxM25xcDB6bzNvYTU5In0.-mGdgCvd0Yy-mWhXTjJcsQ'


def load_data():
    df = pd.read_csv('Dash Data/Supply_v2.csv')
    return df


df = load_data()
cols = df.columns

layout = [
    # Title of the page
    html.Div([
        html.Div(
            html.P('Supply chain by State and Drug Name', style={"fontSize": 20, "font-family": "Halvetica Neue", "textAlign": "center", 'margin-top': 40, 'margin-bottom': 5})
        ),
    ]),
    # Drop down and Map,
    html.Div([
        html.Div(
            dcc.Dropdown(
                id='drug-selected',
                value=['Tylenol'],
                multi=True,
                options=[{'label': i, 'value': i} for i in df['Ingredient/Drug'].unique()],
                style={'margin-bottom': 10},
                placeholder="Select a Drug"
            ),
            className="six columns"),
        html.Div(
            dcc.Dropdown(
                id='state-selected',
                value=['Virginia'],
                multi=True,
                options=[{'label': i, 'value': i} for i in df['State'].unique()],
                style={'margin-bottom': 10},
                placeholder="Select a State"
            ),
            className="six columns"),
        html.Div(
            dcc.Graph(
                id='map-plot',
                config=dict(displayModeBar=False),
            ),
            className="twelve columns")
    ],className="row"),
]
@app.callback(
    Output('map-plot', 'figure'),
    [Input('drug-selected', 'value'),
     Input('state-selected', 'value')],
)
def map_maker(drugs, states):
    """
     Get the option from the drop down and create the map accordingly
    :return:
    """
    trace = []
    for drug in drugs:
        dff = df[df['Ingredient/Drug'] == drug]
        for state in states:
            dfff = dff[dff['State'] == state]
            trace.append(
                go.Scattermapbox(
                    lat = dfff['Latitude'],
                    lon = dfff['Longitude'],
                    mode = 'markers',
                    marker = go.scattermapbox.Marker(
                        size = 13,
                        color = 'rgb(0, 0, 128)',
                        opacity=0.7
                    ),
                    text=str(dfff[['Name of Process', 'Process', 'Score', 'Ingredient/Drug', 'Location']]),
                    hoverinfo = 'text',
                    name=drug
                )
            )
        layout = go.Layout(
            autosize = True,
            hovermode = 'closest',
            showlegend = True,
            height=700,
            margin=dict(l = 20, r = 20, t = 20, b = 20),
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
