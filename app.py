import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, html, dcc, Output, Input
from dash_iconify import DashIconify
from graphs.ingestor import get_data_frame
from graphs.utils import get_trades_by_type, get_df_rows_by_symbol


pd.options.mode.copy_on_write = True

df = get_data_frame("Exchange_1")


# Treemap logic
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
    
    fig.update_layout(template="plotly_dark", title='Click on a cell in the treemap to view line graph')

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
                                html.A(
                                    href="#treemap",
                                    children=(
                                        html.Div(
                                            className="sidemenu-link-container",
                                            children=[
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                            DashIconify(
                                                            icon="mingcute:tree-fill",
                                                            width=20
                                                        ),
                                                        ' Tree Map'
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            )
                        ),
                        
                        html.Div(
                            children=(
                                html.A(
                                    href="#heatmap",
                                    children=(
                                        html.Div(
                                            className="sidemenu-link-container",
                                            children=[
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                            DashIconify(
                                                            icon="mdi:hot",
                                                            width=20
                                                        ),
                                                        ' Heat Map'
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            )
                        ),
                        
                        html.Div(
                            children=(
                                html.A(
                                    href="#acknowledged-time-stock",
                                    children=(
                                        html.Div(
                                            className="sidemenu-link-container",
                                            children=[
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                            DashIconify(
                                                            icon="ant-design:stock-outlined",
                                                            width=20
                                                        ),
                                                        ' Stock'
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            )
                        ),
                        
                        html.Div(
                            children=(
                                html.A(
                                    href="#acknowledged-time-exchange",
                                    children=(
                                        html.Div(
                                            className="sidemenu-link-container",
                                            children=[
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                            DashIconify(
                                                            icon="mdi:exchange",
                                                            width=20
                                                        ),
                                                        ' Exchange'
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            )
                        ),
                        
                        html.Div(
                            children=(
                                html.A(
                                    href="#cancel-time",
                                    children=(
                                        html.Div(
                                            className="sidemenu-link-container",
                                            children=[
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                            DashIconify(
                                                            icon="material-symbols:cancel",
                                                            width=20
                                                        ),
                                                        ' Cancel'
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            )
                        ),
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
                            id="treemap",
                            children=[
                                html.Div(
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
                        ),
                        
                        html.Div(
                            id='heatmap',
                            children=(
                                dcc.Graph(
                                    style={
                                        "height": "98vh",
                                    },
                                    figure=get_graph_data()
                                )
                            )
                        ),
                        
                        html.Div(
                            id='acknowledged-time-stock',
                            children=(
                                dcc.Graph(
                                    style={
                                        "height": "98vh",
                                    },
                                    figure=get_graph_data()
                                )
                            )
                        ),
                        
                        html.Div(
                            id='acknowledged-time-exchange',
                            children=(
                                dcc.Graph(
                                    style={
                                        "height": "98vh",
                                    },
                                    figure=get_graph_data()
                                )
                            )
                        ),
                        
                        html.Div(
                            id='cancel-time',
                            children=(
                                dcc.Graph(
                                    style={
                                        "height": "98vh",
                                    },
                                    figure=get_graph_data()
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
                            children=[
                                html.P(
                                    id="exchange",
                                    children='Choose the exchange you want to analyze'
                                ),
                                dcc.Dropdown(
                                    ['Exchange 1', 'Exchange 2', 'Exchange 3'], 
                                    'Exchange 1', 
                                    id='exchange-dropdown'
                                ),
                            ]
                        )
                    ]
                )
            )
        )
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


@app.callback(
    Output('exchange', 'children'),
    Input('exchange-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run(debug=True)
