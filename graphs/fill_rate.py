from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ingestor import get_data_frame
from utils import get_trades_by_type, get_duration_of_x_and_y

df = get_duration_of_x_and_y(get_data_frame("Exchange_1"), "CancelRequest", "CancelAcknowledged")

print(df)

def get_heatmap_figure():
    fig = px.density_heatmap(df, x="TimeStamp_x", y="XYDuration")
    return fig

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Heatmap Test', style={'textAlign':'center'}),
    dcc.Graph(id='fill-rate-heatmap', figure=get_heatmap_figure())
])

if __name__ == '__main__':
    app.run(debug=True)
