from ingestor import get_data_frame
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = get_data_frame("Exchange_1")


app.layout = html.Div([
    html.H4('Stock price analysis'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select stock:"),
    fig = px.line(df, x='TimeStampEpoch', y="PRQ83")
    dcc.Graph(figure=fig)
    
])



app.run_server(debug=True)