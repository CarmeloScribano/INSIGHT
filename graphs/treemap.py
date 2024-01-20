from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ingestor import get_data_frame

df = get_data_frame("Exchange_1")

app = Dash(__name__)

symbol_counts = df['Symbol'].value_counts()

# Create a new DataFrame for Plotly treemap
treemap_data = pd.DataFrame({'Symbol': symbol_counts.index, 'Count': symbol_counts.values})

# Create a treemap using Plotly Express
fig = px.treemap(treemap_data, path=['Symbol'], values='Count', title='Symbol Frequency Treemap')

app.layout = html.Div([
    html.H1("Symbol Frequency Treemap"),
    dcc.Graph(
        id='symbol-treemap',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
