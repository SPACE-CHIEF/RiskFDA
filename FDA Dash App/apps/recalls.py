import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import us
from app import app
import os
import dash

PATH = 'Dash Data/Supply_v2.csv'


def load_data(path):
    df = pd.read_csv(PATH)
    return df


recalls = load_data(PATH)
print(recalls.columns)
# Format the date to use it in a time series graph
recalls['Date of Process'] = pd.to_datetime(recalls['Date of Process'], infer_datetime_format=True)
layout = [
    # Title of the page
    html.Div([
        html.Div(
            html.P('Recalls by Drug Name and Facility',
                   style={"fontSize": 20, "font-family": "Halvetica Neue", "textAlign": "center", 'margin-top': 40,
                          'margin-bottom': 5})
        ),
    ]),
    # Drop downs and time series graph
        html.Div([
            html.Div([
                html.Div(
                    dcc.Dropdown(
                    id='drug-selected',
                    value=['Virginia'],
                    multi=True,
                    options=[{'label': i, 'value': i} for i in recalls['Ingredient/Drug'].unique()],
                    style={'margin-bottom': 10, "float": "center"},
                    placeholder="Select a Drug"),
                className="one-fourth column"),
                html.Div(
                    dcc.Dropdown(
                    id='facility-selected',
                    value=['3M'],
                    multi=True,
                    options=[{'label': i, 'value': i} for i in recalls['Name of Process'].unique()],
                    style={'margin-bottom': 10, "float": "center"},
                    placeholder="Select a facility"),
                className="one-fourth column"),
        ], className="fixed-gutter-grid"),
                html.Div(
                    dcc.Graph(
                    id='time-graph'),
                    className="one-half column")
    ], className="l-wrap")
]

@app.callback(
    Output('time-graph', 'figure'),
    [Input('drug-selected', 'value'),
     Input('facility-selected', 'value')],
)
def time_graph(drugs, facilities):
    nai_trace = []
    oai_trace = []
    vai_trace = []
    for drug in drugs:
        recalls_2 = recalls[recalls['Ingredient/Drug'] == drug]
        for facility in facilities:
            recalls_3 = recalls_2[recalls_2['Name of Process'] == facility]
            nai_trace.append(
                go.Scatter(
                    x=recalls_3[recalls_3['Inspection Classification'] == 'NAI']['Date of Process'],
                    y=recalls_3[recalls_3['Inspection Classification'] == 'NAI']['Score'],
                    mode='lines',
                    opacity=0.7,
                    textposition='bottom center'
                )
            )
            oai_trace.append(
                go.Scatter(
                    x=recalls_3[recalls_3['Inspection Classification'] == 'OAI']['Date of Process'],
                    y=recalls_3[recalls_3['Inspection Classification'] == 'OAI']['Score'],
                    mode='lines',
                    opacity=0.7,
                    textposition='bottom center'
                )
            )
            vai_trace.append(
                go.Scatter(
                    x=recalls_3[recalls_3['Inspection Classification'] == 'VAI']['Date of Process'],
                    y=recalls_3[recalls_3['Inspection Classification'] == 'VAI']['Score'],
                    mode='lines',
                    opacity=0.7,
                    textposition='bottom center'
                )
            )
            traces = [oai_trace, vai_trace, nai_trace]
            data = [val for sublist in traces for val in sublist]
            layout = go.Layout(
                colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                height=600,
                xaxis={"title": "Date",
                       'rangeselector': {
                           'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                            {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                            {'step': 'all'}])},
                       'rangeslider': {'visible': True}, 'type': 'date'},
                yaxis={"title": "Price (USD)"}
            )
            return {'data': data, 'layout': layout}
