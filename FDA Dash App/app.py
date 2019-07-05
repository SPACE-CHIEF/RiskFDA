import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True