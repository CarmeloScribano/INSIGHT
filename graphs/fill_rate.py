import pandas as pd
import plotly.graph_objects as go
from .ingestor import get_data_frame
from .utils import get_duration_of_x_and_y

raw_df = get_data_frame("Exchange_1")
df = get_duration_of_x_and_y(raw_df, "NewOrderRequest", "NewOrderAcknowledged")

DEFAULT_THRESHOLD = 30

def merge_raw_with_duration():
    return pd.merge(raw_df, df, on="OrderID", how="outer")

def get_heatmap_figure(threshold):

    threshold = threshold or DEFAULT_THRESHOLD

    mdf = merge_raw_with_duration()

    mdf['AboveThreshold'] = mdf['XYDuration'] < threshold

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
