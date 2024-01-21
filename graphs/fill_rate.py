import pandas as pd
import plotly.graph_objects as go

from .utils import get_duration_of_x_and_y

DEFAULT_THRESHOLD = 60

def merge_raw_with_duration(raw_df, df):
    return pd.merge(raw_df, df, on='OrderID', how='outer')

def get_heatmap_figure(raw_df, threshold):
    threshold = threshold or DEFAULT_THRESHOLD

    df = get_duration_of_x_and_y(raw_df, 'NewOrderRequest', 'NewOrderAcknowledged')

    mdf = merge_raw_with_duration(raw_df, df)

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
        colorscale=[[0, 'rgb(255,0,0)'], [1, 'rgb(0,255,0)']]
    ))

    fig.update_layout(title='Fill Rate Heatmap',
                    xaxis_title='Timestamp',
                    yaxis_title='Symbol',
                    template='plotly_dark')

    return fig
