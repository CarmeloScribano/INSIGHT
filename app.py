import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, html, dcc, Output, Input
from dash_iconify import DashIconify
from graphs.ingestor import get_data_frame
from graphs.utils import get_trades_by_type, get_df_rows_by_symbol
from graphs.carmGraph import fig

pd.options.mode.copy_on_write = True

df = get_data_frame("Exchange_1")

def get_acked_trades():
    return get_trades_by_type(df, "NewOrderAcknowledged")

def get_merged_df(left, right, key):
    return pd.merge(left, right, on=key)

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
    
    fig.update_layout(template="plotly_dark")

    return fig
    

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            className="sidemenu",
            children=(
                html.Div(
                    children= [
                        html.Div(
                            children=(
                                DashIconify(
                                    icon="ion:logo-github",
                                    width=30
                                )
                            )
                        ),

                        html.Div(
                            children=(
                                DashIconify(
                                    icon="ion:logo-github",
                                    width=30
                                )
                            )
                        ),

                        html.Div(
                            children=(
                                DashIconify(
                                    icon="ion:logo-github",
                                    width=30
                                )
                            )
                        ),

                        html.Div(
                            children=(
                                DashIconify(
                                    icon="ion:logo-github",
                                    width=30
                                )
                            )
                        ),

                        html.Div(
                            children=(
                                DashIconify(
                                    icon="ion:logo-github",
                                    width=30
                                )
                            )
                        )
                    ]
                )                
            )
        ),
        
        html.Div(
            className="main",
            children=(
                html.Div(
                    className="main-container",
                    children=[
                        html.Div(
                            className="graph1", 
                            children=(
                                dcc.Graph(
                                    id='symbol-treemap',
                                    style={
                                        "height": "48vh",
                                    },
                                    figure=get_graph_data()
                                )
                            )
                        ),

                        html.Div(
                            className="graph2", 
                            children=(
                                dcc.Graph(
                                    id='example-graph2',
                                    style={
                                        "height": "48vh",
                                    },
                                    figure=fig
                                )
                            )
                        ),

                        html.Div(
                            className="graph3", 
                            children=(
                                dcc.Graph(
                                    id='line-graph',
                                    style={
                                        "height": "48vh",
                                    }
                                )
                            )
                        )
                    ]
                )
            )
        ),

        html.Div(
            className="static-data",
            children=(
                html.Div(
                    className="static-data-container",
                    children=[
                        html.Div(
                            children=(
                                dcc.Graph(
                                    id='static-data-graph1',
                                    figure=fig
                                )
                            )
                        ),

                        html.P(
                            className="timestamp",
                            children=('09:29:34')
                        )
                    ]
                )
            )
        ),
    ]
)


# Treemap click behaviour
@app.callback(
    Output('line-graph', 'figure'),
    [Input('symbol-treemap', 'clickData')]
)
def update_line_graph(click_data):
    if click_data is not None:
        selected_symbol = click_data['points'][0]['label']
        line_fig = get_line_graph_data(selected_symbol)
        return line_fig

    return get_default_line_graph()


if __name__ == '__main__':
    app.run(debug=True)
