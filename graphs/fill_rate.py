from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ingestor import get_data_frame
from utils import get_trades_by_type, get_duration_of_x_and_y
import plotly.graph_objects as go

raw_df = get_data_frame("Exchange_1")
df = get_duration_of_x_and_y(raw_df, "NewOrderRequest", "NewOrderAcknowledged")

# print(df)

def merge_raw_with_duration():
    return pd.merge(raw_df, df, on="OrderID", how="outer")

merge_raw_with_duration()

def get_heatmap_figure():
    # Assuming merge_raw_with_duration returns a DataFrame with columns: 'Symbol', 'XYDuration', 'TimeStamp_y'
    mdf = merge_raw_with_duration()
    THRESHOLD = 60
    mdf['AboveThreshold'] = mdf['XYDuration'] > THRESHOLD

    # Round the timestamps to 5-second intervals
    mdf['TimeStamp_rounded'] = mdf['TimeStamp_x'].dt.round('5s')

    # Convert 'AboveThreshold' to boolean
    mdf['AboveThreshold'] = mdf['AboveThreshold'].astype(bool)

    aggregated_df = mdf.groupby(['Symbol', 'TimeStamp_rounded']).agg({'AboveThreshold': lambda x: (x.sum() / len(x)) * 100}).reset_index()

    # Create a heatmap using Plotly Graph Objects
    fig = go.Figure(go.Heatmap(
        z=aggregated_df['AboveThreshold'],
        x=aggregated_df['TimeStamp_rounded'],
        y=aggregated_df['Symbol'],
        # colorscale='Viridis'
        colorscale=[[0, 'rgb(255,0,0)'], [1, 'rgb(0,255,0)']]
    ))

    # Customize the layout
    fig.update_layout(title='Heatmap Aggregated by 5 Seconds',
                    xaxis_title='Timestamp',
                    yaxis_title='Symbol',
                    template="plotly_dark")

    return fig

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Heatmap Test', style={'textAlign':'center'}),
    dcc.Graph(id='fill-rate-heatmap', figure=get_heatmap_figure())
])

if __name__ == '__main__':
    app.run(debug=True)
