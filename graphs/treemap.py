from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ingestor import get_data_frame

df = get_data_frame("Exchange_1")

def get_acked_trades():
    return df[df['MessageType'] == 'NewOrderAcknowledged']

def get_stock_info():
    grouped_df = df.groupby('Symbol')

    # Calculate min, max, and average prices for each stock
    summary_df = grouped_df['OrderPrice'].agg(['min', 'max', 'mean']).reset_index()
    return summary_df

def get_graph_data(): 
    get_acked_trades()

    stats = get_stock_info()

    merged_df = pd.merge(df, stats, on='Symbol')

    symbol_counts = merged_df['Symbol'].value_counts()

    # print(merged_df.min)


    # Create a new DataFrame for Plotly treemap
    treemap_data = pd.DataFrame({'Symbol': symbol_counts.index, 'Count': symbol_counts.values})

    # Create a treemap using Plotly Express with animation
    fig = px.treemap(treemap_data, path=['Symbol'], values='Count', title='Symbol Frequency Treemap')
    fig.update_traces(hovertemplate='<b>Stock:</b> %{label}<br><b>Volume Traded:</b> %{value}')
    return fig

def get_min_price(symbol):
    # Find the minimum price for a given symbol
    return df[df['Symbol'] == symbol]['OrderPrice'].min()

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symbol Frequency Treemap"),
    dcc.Graph(
        id='symbol-treemap',
        figure=get_graph_data()
    )
])


if __name__ == '__main__':
    app.run(debug=True)
