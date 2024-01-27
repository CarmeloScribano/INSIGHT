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
        # Top Statistics & Treemap
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
                                                        DashIconify(icon='material-symbols-light:search', className='grey', width=30),
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
        

        # Divider Bar
        html.Hr(
            style={
                'width': '50vw'
            }
        ),


        # Main Graph - Trade Volume
        html.Div(
            className='main-container hidden',
            children=(
                html.Div(
                    className='main-container-toggle',
                    children=(
                        DashIconify(icon='bi:chevron-left', className='white', style={'paddingRight': '1vw'}, width=60),
                    )
                ),

                html.Div(
                    children=[
                        html.Div(
                            className='horizontal-align',
                            children=[
                                html.Div(
                                    className='anomaly-container text-center',
                                    children=(
                                        html.Div(
                                            children=[
                                                html.P(className='main-statistic-title', children='Anomaly Detected'),
                                                html.P(className='anomaly-text', children='09:30:23')
                                            ]
                                        )
                                    )
                                ),
                                html.Div(
                                    className='lowest-delay-container text-center',
                                    children=(
                                        html.Div(
                                            children=[
                                                html.P(className='main-statistic-title', children='Lowest Delay'),
                                                html.P(className='delay-text', children='0.1')
                                            ]
                                        )
                                    )
                                ),
                                html.Div(
                                    className='highest-delay-container text-center',
                                    children=(
                                        html.Div(
                                            children=[
                                                html.P(className='main-statistic-title', children='Highest Delay'),
                                                html.P(className='delay-text', children='3.4')
                                            ]
                                        )
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className='main-graph',
                            children=(
                                dcc.Graph(
                                    id='line-graph',
                                    style={
                                        'height': '45vh',
                                        'width': '90vw'
                                    }
                                )
                            )
                        )
                    ]
                ),
                
                html.Div(
                    className='main-container-toggle',
                    children=(
                        DashIconify(icon='bi:chevron-right', className='white', style={'paddingLeft': '1vw'}, width=60),
                    )
                )
            )
        ),
    

        # Main Graph - Acknowledged Delay
        html.Div(
            className='main-container hidden',
            children=(
                html.Div(
                    className='main-container-toggle',
                    children=(
                        DashIconify(icon='bi:chevron-left', className='white', style={'paddingRight': '1vw'}, width=60),
                    )
                ),

                html.Div(
                    className='horizontal-align',
                    children=[
                        html.Div(
                            className='graph',
                            children=(
                                dcc.Graph(
                                    id='bubble-stock-id-acked',
                                    style={
                                        'height': '60vh',
                                        'width': '60vw',
                                        'margin': '2vh 0 1vh 0'
                                    }
                                ) 
                            )
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    className='anomaly-container-delay text-center',
                                    children=(
                                        html.Div(
                                            children=[
                                                html.P(className='main-statistic-title', children='Anomaly Detected'),
                                                html.P(className='anomaly-text', children='09:30:23')
                                            ]
                                        )
                                    )
                                ),
                                html.Div(
                                    className='horizontal-align',
                                    children=[
                                        html.Div(
                                            className='lowest-delay-container-delay text-center',
                                            children=(
                                                html.Div(
                                                    children=[
                                                        DashIconify(icon='ph:minus-fill', className='delay-icon', color='#00664B', width=100),
                                                        html.P(className='main-statistic-title', children='Lowest Delay'),
                                                        html.P(className='delay-text', children='0.1')
                                                    ]
                                                )
                                            )
                                        ),
                                        html.Div(
                                            className='highest-delay-container-delay text-center',
                                            children=(
                                                html.Div(
                                                    children=[
                                                        DashIconify(icon='ph:plus-fill', className='delay-icon', color='#B4260F', width=100),
                                                        html.P(className='main-statistic-title', children='Highest Delay'),
                                                        html.P(className='delay-text', children='3.4')
                                                    ]
                                                )
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                    ]
                ),
                
                html.Div(
                    className='main-container-toggle',
                    children=(
                        DashIconify(icon='bi:chevron-right', className='white', style={'paddingLeft': '1vw'}, width=60),
                    )
                )
            )
        ),


        # Main Graph - Cancelled Delay
        html.Div(
            className='main-container',
            children=(
                html.Div(
                    className='main-container-toggle',
                    children=(
                        DashIconify(icon='bi:chevron-left', className='white', style={'paddingRight': '1vw'}, width=60),
                    )
                ),

                html.Div(
                    className='horizontal-align',
                    children=[
                        html.Div(
                            className='graph',
                            children=(
                                dcc.Graph(
                                    id='bubble-stock-id',
                                    style={
                                        'height': '60vh',
                                        'width': '60vw',
                                        'margin': '2vh 0 1vh 0'
                                    }
                                )
                            )
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    className='anomaly-container-delay text-center',
                                    children=(
                                        html.Div(
                                            children=[
                                                html.P(className='main-statistic-title', children='Anomaly Detected'),
                                                html.P(className='anomaly-text', children='09:30:23')
                                            ]
                                        )
                                    )
                                ),
                                html.Div(
                                    className='horizontal-align',
                                    children=[
                                        html.Div(
                                            className='lowest-delay-container-delay text-center',
                                            children=(
                                                html.Div(
                                                    children=[
                                                        DashIconify(icon='ph:minus-fill', className='delay-icon', color='#00664B', width=100),
                                                        html.P(className='main-statistic-title', children='Lowest Delay'),
                                                        html.P(className='delay-text', children='0.1')
                                                    ]
                                                )
                                            )
                                        ),
                                        html.Div(
                                            className='highest-delay-container-delay text-center',
                                            children=(
                                                html.Div(
                                                    children=[
                                                        DashIconify(icon='ph:plus-fill', className='delay-icon', color='#B4260F', width=100),
                                                        html.P(className='main-statistic-title', children='Highest Delay'),
                                                        html.P(className='delay-text', children='3.4')
                                                    ]
                                                )
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                    ]
                ),
                
                html.Div(
                    className='main-container-toggle',
                    children=(
                        DashIconify(icon='bi:chevron-right', className='white', style={'paddingLeft': '1vw'}, width=60),
                    )
                )
            )
        ),
    

        # Chart Links
        html.Div(
            className='',
            children=[
                html.Div(
                    className='text-center',
                    children=[
                        html.Button(
                            className='chart-menu-button active-chart',
                            children=[
                                'Trade Volume',
                                html.Div(
                                    className='selected-item'
                                )
                            ]
                        ),
                        html.Button(
                            className='chart-menu-button',
                            children=[
                                'Acknowledged Delay',
                                html.Div(
                                    className='selected-item hidden'
                                )
                            ]
                        ),
                        html.Button(
                            className='chart-menu-button',
                            children=[
                                'Fill Rate',
                                html.Div(
                                    className='selected-item hidden'
                                )
                            ]
                        ),
                        html.Button(
                            className='chart-menu-button',
                            children=[
                                'Cancelled Delay',
                                html.Div(
                                    className='selected-item hidden'
                                )
                            ]
                        )
                    ]
                )
            ]
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


# Callback for Acked graph
@app.callback(
    Output('bubble-stock-id-acked', 'figure'),
    Input('symbol-treemap', 'clickData'),
    Input('exchange-dropdown', 'value'),
)
def update_acked_output(click_data, children):
    if click_data is not None:
        selected_symbol = click_data['points'][0]['label']
        line_fig = get_acked_figure(get_df(), selected_symbol)
        return line_fig

    return get_default_line_graph()


# Callback for Stock ID graph
@app.callback(
        Output('bubble-stock-id', 'figure'),
        Input('symbol-treemap', 'clickData'),
        Input('exchange-dropdown', 'value'))
def update_output_cancelled(click_data, children):
    if click_data is not None:
        selected_symbol = click_data['points'][0]['label']
        line_fig = get_cancelled_graph(get_df(), current_exchange, selected_symbol)
        return line_fig

    return get_default_line_graph()


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
