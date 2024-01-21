from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
from ingestor import get_data_frame
from utils import get_trades_by_type, get_duration_of_x_and_y
import plotly.graph_objects as go

raw_df = get_data_frame("Exchange_1")
df = get_duration_of_x_and_y(raw_df, "NewOrderRequest", "NewOrderAcknowledged")

DEFAULT_THRESHOLD = 30

def merge_raw_with_duration():
    return pd.merge(raw_df, df, on="OrderID", how="outer")

def get_heatmap_figure(threshold):

    threshold = threshold or DEFAULT_THRESHOLD

    mdf = merge_raw_with_duration()

    mdf['AboveThreshold'] = mdf['XYDuration'] > threshold

    mdf['TimeStamp_rounded'] = mdf['TimeStamp_x'].dt.round('5s')

    mdf['AboveThreshold'] = mdf['AboveThreshold'].astype(bool)

    aggregated_df = mdf.groupby(['Symbol', 'TimeStamp_rounded']).agg({'AboveThreshold': lambda x: (x.sum() / len(x)) * 100}).reset_index()

    fig = go.Figure(go.Heatmap(
        z=aggregated_df['AboveThreshold'],
        x=aggregated_df['TimeStamp_rounded'],
        y=aggregated_df['Symbol'],
        zmin=0,
        zmax=100,
        # colorscale='Viridis'
        colorscale=[[0, 'rgb(255,0,0)'], [1, 'rgb(0,255,0)']]
    ))

    fig.update_layout(title='Heatmap Aggregated by 5 Seconds',
                    xaxis_title='Timestamp',
                    yaxis_title='Symbol',
                    template="plotly_dark")

    return fig

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Heatmap Test', style={'textAlign':'center'}),
    dcc.Graph(id='fill-rate-heatmap', figure=get_heatmap_figure(DEFAULT_THRESHOLD)),
    dcc.Input(id='input-fill-threshold', type='number', placeholder='30μs'),
    html.Button(id='submit-fill-threshold', n_clicks=0, children='Update'),
    html.P(id="test", children=f'Current Threshold: {DEFAULT_THRESHOLD} microseconds')
])

@app.callback(
    Output('fill-rate-heatmap', 'figure'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_heatmap(n_clicks, threshold):
    return get_heatmap_figure(threshold)

@app.callback(
    Output('test', 'children'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_current_threshold(n_clicks, threshold):
    return f"Current Threshold: {threshold or DEFAULT_THRESHOLD} microseconds"

if __name__ == '__main__':
    app.run(debug=True)
