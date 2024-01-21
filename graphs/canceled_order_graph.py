import json
from ingestor import get_data_frame
from utils import get_trades_by_type, get_duration_of_x_and_y
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
exchange = "Exchange_2"
df = get_data_frame(exchange)


app = Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input-stock-state', type='text', value='XXRQC'),
    html.Button(id='submit-stock-state', n_clicks=0, children='Submit'),
    dcc.Graph(
        id= 'bubble-stock-id')])

@callback(Output('bubble-stock-id', 'figure'),
          Output('input-stock-state', 'value'),
              Input('submit-stock-state', 'n_clicks'),
              State('input-stock-state', 'value'))
def update_output(n_clicks, stock_value):
    dff = df[df['Symbol'] == stock_value]
    cancel_var = "CancelAcknowledged"
    if exchange == "Exchange_2":
        cancel_var = "Cancelled"
    dff = get_duration_of_x_and_y(dff,"CancelRequest", cancel_var)
    fig = px.scatter(dff,x='TimeStamp_x',y="XYDuration",color="XYDuration")
    return fig,stock_value

if __name__ == '__main__':
    app.run(debug=True)