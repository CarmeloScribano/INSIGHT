import json
from ingestor import get_data_frame
from utils import get_trades_by_type
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd

df = get_data_frame("Exchange_1")

new_order_requests = get_trades_by_type(df=df, msg_type="CancelRequest").sort_values(by='TimeStamp')
order_acknowledges = df.groupby(['OrderID']).apply(lambda x: x[x["MessageType"] == "CancelAcknowledged"])
new_order_requests.reset_index(drop = True, inplace = True)
order_acknowledges.reset_index(drop = True, inplace = True)
merged_pd = new_order_requests.merge(order_acknowledges, on="OrderID")[["TimeStamp_x", "TimeStamp_y"]]
merged_pd["OrderAcknowledgedDuration"] = merged_pd["TimeStamp_y"] - merged_pd["TimeStamp_x"]
print(merged_pd)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input-stock-state', type='text', value='PRQ83'),
    html.Button(id='submit-stock-state', n_clicks=0, children='Submit'),
    dcc.Graph(
        id= 'bubble-stock-id')])

@callback(Output('bubble-stock-id', 'figure'),
              Input('submit-stock-state', 'n_clicks'),
              State('input-stock-state', 'value'))
def update_output(n_clicks, stock_value):
    dff = df[df['Symbol'] == stock_value]
    fig = px.scatter(merged_pd,x='TimeStamp_x',y="OrderAcknowledgedDuration",size="OrderAcknowledgedDuration")
    return fig

if __name__ == '__main__':
    app.run(debug=True)