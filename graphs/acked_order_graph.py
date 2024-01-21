import json
from ingestor import get_data_frame
from utils import get_duration_of_x_and_y
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
exchange = "Exchange_1"
df = get_data_frame(exchange)


app = Dash(__name__)

app.layout = html.Div([
    html.Div("Acknowldedge orders within a Scatter plot"),
    dcc.Input(id='input-stock-state-acked', type='text', value='5AV4I'),
    html.Button(id='submit-stock-state', n_clicks=0, children='Submit'),
    dcc.Graph(
        id= 'bubble-stock-id')])

@callback(Output('bubble-stock-id', 'figure'),
          Output('input-stock-state-acked', 'value'),
              Input('submit-stock-state', 'n_clicks'),
              State('input-stock-state-acked', 'value'))
def update_output(n_clicks, stock_value):
    dff = df[df['Symbol'] == stock_value]
    dff = get_duration_of_x_and_y(dff,"NewOrderRequest", "NewOrderAcknowledged")
    fig = px.scatter(dff,x='TimeStamp_x',y="XYDuration",color="XYDuration")
    return fig,stock_value

if __name__ == '__main__':
    app.run(debug=True)