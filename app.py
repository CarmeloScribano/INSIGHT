import pandas as pd
import plotly.graph_objects as go

from dash import Dash, html, dcc, Output, Input, State
from dash_iconify import DashIconify
from graphs.ingestor import get_data_frame
from graphs.treemap import get_graph_data, get_line_graph_data, get_default_line_graph
from graphs.fill_rate import DEFAULT_THRESHOLD, get_heatmap_figure
from graphs.acked_order_graph import get_acked_figure
from graphs.cancelled_order_graph import get_cancelled_graph

pd.options.mode.copy_on_write = True

DFS = {
    'Exchange 1' : get_data_frame('Exchange_1'),
    'Exchange 2' : get_data_frame('Exchange_2'),
    'Exchange 3' : get_data_frame('Exchange_3')
}

current_exchange = 'Exchange 1'

def get_df():
    return DFS[current_exchange]

def set_exchange(exchange):
    global current_exchange
    current_exchange = exchange

app = Dash(__name__)

app.title = 'IN$IGHT'

app.layout = html.Div(
    children=[
        html.Div(
            className='horizontal-align', 
            children=[
                html.Div(
                    className='general-statistics',
                    children=[
                        html.Div(
                            className='horizontal-align', 
                            children=[
                                html.Div(
                                    className='statistic-container time-statistic',
                                    children=[
                                        html.Div(
                                            className='text-center',
                                            children=[
                                                DashIconify(icon='dashicons:clock', width=40),
                                                html.P(id='time-title', className='statistic-title', children='Total Time'),
                                                html.P(id='time', className='statistic-text', children='56m')
                                            ]
                                        )
                                    ]
                                ),

                                html.Div(
                                    className='statistic-container exchanges-statistic',
                                    children=[
                                        html.Div(
                                            className='text-center',
                                            children=[
                                                DashIconify(icon='mdi:graph-line', width=40),
                                                html.P(id='exchanges-title', className='statistic-title', children='Total Exchanges'),
                                                html.P(id='exchanges', className='statistic-text', children='5,435')
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='horizontal-align', 
                            children=[
                                html.Div(
                                    className='statistic-container exchange-statistic',
                                    children=[
                                        html.Div(
                                            className='text-center',
                                            children=[
                                                html.P(id='exchange-title', className='statistic-title', children='Current Exchange'),
                                                dcc.Dropdown(
                                                    id='exchange-dropdown',
                                                    options=['Exchange 1', 'Exchange 2', 'Exchange 3'], 
                                                    value='Exchange 1'
                                                )
                                            ]
                                        )
                                    ]
                                ),

                                html.Div(
                                    className='statistic-container search-statistic',
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    className='horizontal-align',
                                                    children=[
                                                        DashIconify(icon='material-symbols-light:search', className='grey', width=40),
                                                        dcc.Dropdown(
                                                            id='input',
                                                            options=['QBG5', 'TTTT', 'FGHR'],
                                                            placeholder='Search Option',
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),

                html.Div(
                    className='graph',
                    children=(
                        dcc.Graph(id='symbol-treemap', style={
                            'height': '30vh',
                            'width': '68vw',
                            'margin': '0.5vw 0.5vw 0.5vh 0.5vw'
                        })
                    )
                )
            ]
        ),
        
        html.Hr(
            style={
                'width': '75vw'
            }
        ),

        html.Div(
            children=(
                dcc.Graph(
                    id='line-graph',
                    style={
                        'height': '43vh',
                    }
                )
            )
        )
    ]
)


# Callback for Treemap graph
@app.callback(
    Output('symbol-treemap', 'figure'),
    [Input('exchange-title', 'children')]
)
def update_treemap_figure(children):
    return get_graph_data(get_df())

@app.callback(
    Output('line-graph', 'figure'),
    [Input('symbol-treemap', 'clickData')]
)
def update_line_graph(click_data):
    if click_data is not None:
        selected_symbol = click_data['points'][0]['label']
        line_fig = get_line_graph_data(get_df(), selected_symbol)
        return line_fig

    return get_default_line_graph()


# # Callback for Acked graph
# @app.callback(
#     Output('bubble-stock-id-acked', 'figure'),
#     Input('symbol-treemap', 'clickData'),
#     Input('exchange', 'children'),
# )
# def update_acked_output(click_data, children):
#     if click_data is not None:
#         selected_symbol = click_data['points'][0]['label']
#         line_fig = get_acked_figure(get_df(), selected_symbol)
#         return line_fig

#     return get_default_line_graph()


# # Callback for Stock ID graph
# @app.callback(
#         Output('bubble-stock-id', 'figure'),
#         Input('symbol-treemap', 'clickData'),
#         Input('exchange', 'children'))
# def update_output_cancelled(click_data, children):
#     if click_data is not None:
#         selected_symbol = click_data['points'][0]['label']
#         line_fig = get_cancelled_graph(get_df(), current_exchange, selected_symbol)
#         return line_fig

#     return get_default_line_graph()

# # Callbacks for Fill Rate graph
# @app.callback(
#     Output('fill-rate-heatmap', 'figure'),
#     Input('submit-fill-threshold', 'n_clicks'),
#     Input('exchange', 'children'),
#     State('input-fill-threshold', 'value')
# )
# def update_heatmap(n_clicks, children, threshold):
#     return get_heatmap_figure(get_df(), threshold)

# @app.callback(
#     Output('current-threshold', 'children'),
#     Input('submit-fill-threshold', 'n_clicks'),
#     State('input-fill-threshold', 'value')
# )
# def update_current_threshold(n_clicks, threshold):
#     return f'Current Threshold: {threshold or DEFAULT_THRESHOLD} microseconds'


# Callback for the exchange dropdownlist
@app.callback(
    Output('exchange-title', 'children'),
    Input('exchange-dropdown', 'value')
)
def update_output(value):
    set_exchange(value)
    return 'Current Exchange'


if __name__ == '__main__':
    app.run(debug=True)
