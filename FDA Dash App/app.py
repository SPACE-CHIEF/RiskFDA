import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

#STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

server = flask.Flask(__name__)
external_stylesheets = [
    'https://github.com/averma1/ladyphideas/blob/master/css/style.css'
]
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True