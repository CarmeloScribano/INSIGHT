from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ingestor import get_data_frame
from utils import get_trades_by_type

df = get_data_frame("Exchange_1")

def get_acked_trades():
    return get_trades_by_type(df, "NewOrderAcknowledged")

def get_graph_data(): 
    symbol_counts = get_acked_trades()['Symbol'].value_counts()

    # Create a new DataFrame for Plotly treemap
    treemap_data = pd.DataFrame({'Symbol': symbol_counts.index, 'Count': symbol_counts.values})

    # Create a treemap using Plotly Express with animation
    fig = px.treemap(treemap_data, path=['Symbol'], values='Count', title='Symbol Frequency Treemap')
    fig.update_traces(hovertemplate='<b>Stock:</b> %{label}<br><b>Volume Traded:</b> %{value}')
    return fig

def get_line_graph_data(selected_symbol):
    # Filter data based on the selected symbol
    filtered_data = get_acked_trades()[get_acked_trades()['Symbol'] == selected_symbol]

    # Create a line graph for 30s intervals
    line_fig = px.line(filtered_data, x='TimeStamp', y='OrderPrice', title=f'Line Graph for Symbol: {selected_symbol}')
    return line_fig

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
