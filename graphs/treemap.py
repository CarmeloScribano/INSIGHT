from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from .ingestor import get_data_frame
from .utils import get_trades_by_type, get_df_rows_by_symbol

pd.options.mode.copy_on_write = True

df = get_data_frame("Exchange_1")

def get_acked_trades():
    return get_trades_by_type(df, "NewOrderAcknowledged")

def get_volume_df():
    symbol_counts = get_acked_trades()['Symbol'].value_counts()

    treemap_data = pd.DataFrame({'Symbol': symbol_counts.index, 'Count': symbol_counts.values})
    return treemap_data

def get_graph_data(): 
    treemap_data = get_volume_df()
    fig = px.treemap(treemap_data, template="plotly_dark", path=['Symbol'], values='Count', title='Symbol Frequency Treemap')
    fig.update_traces(hovertemplate='<b>Stock:</b> %{label}<br><b>Volume Traded:</b> %{value}')
    return fig

def get_line_graph_data(selected_symbol, max_points=100):
    stock_data = get_acked_trades()
    target_df = get_df_rows_by_symbol(stock_data, selected_symbol)

    target_df['TimeStamp'] = pd.to_datetime(target_df['TimeStamp'])

    target_df.set_index('TimeStamp', inplace=True)

    target_df_copy = target_df.copy()

    resampled_df = target_df_copy.resample('5s').size().reset_index(name='TradeCount')
    resampled_df = resampled_df.tail(max_points)

    fig = go.Figure(data=go.Scatter(x=[resampled_df['TimeStamp'].min()], y=[resampled_df['TradeCount'].min()],
                                   mode='markers',
                                   marker=dict(color='rgba(255, 0, 0, 0.8)', size=10),
                                   name='Trade Count'))
    
    fig.update_layout(template="plotly_dark")

    frames = [
        go.Frame(data=go.Scatter(x=resampled_df['TimeStamp'][:i+1],
                                 y=resampled_df['TradeCount'][:i+1],
                                 mode='markers',
                                 marker=dict(color='rgba(255, 0, 0, 0.8)', size=10),
                                 name='Trade Count'),
                 name=str(i))
        for i in range(1, len(resampled_df)+1)
    ]

    frames.append(go.Frame(data=go.Scatter(x=resampled_df['TimeStamp'],
                                           y=resampled_df['TradeCount'],
                                           mode='lines+markers',
                                           marker=dict(color='rgba(255, 0, 0, 0.8)', size=10),
                                           line=dict(color='rgba(255, 0, 0, 0.8)', width=2),
                                           name='Trade Count'),
                           name='Final'))

    fig.frames = frames

    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play',
                                            method='animate', args=[None, dict(frame=dict(duration=250, redraw=True), fromcurrent=True)])])])

    return fig

def get_default_line_graph():
    fig = go.Figure(data=go.Scatter(x=[""], y=[""],
            mode='markers',
            marker=dict(color='rgba(255, 0, 0, 0.8)', size=10),
            name='Trade Count'))
    
    fig.update_layout(template="plotly_dark", title='Click on a cell in the treemap to view line graph')

    return fig


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symbol Frequency Treemap"),
    dcc.Graph(
        id='symbol-treemap',
        figure=get_graph_data()
    ),
    dcc.Graph(
        id='line-graph',
    )
])

@app.callback(
    Output('line-graph', 'figure'),
    [Input('symbol-treemap', 'clickData')]
)
def update_line_graph(click_data):
    if click_data is not None:
        # Extract the selected symbol from the click data
        selected_symbol = click_data['points'][0]['label']

        # Get line graph data for the selected symbol
        line_fig = get_line_graph_data(selected_symbol)

        return line_fig

    # If no cell is clicked, hide the graph
    return {'data': [], 'layout': {'title': 'Click on a cell in the treemap to view line graph'}, 'frames': []}

if __name__ == '__main__':
    app.run(debug=True)
