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

app.layout = html.Div(
    children=[
        html.Div(
            className='sidemenu',
            children=(
                html.Div(
                    children= [
                        html.Div(
                            children=(
                                html.A(
                                    href='#treemap',
                                    children=(
                                        html.Div(
                                            className='sidemenu-link-container',
                                            children=(
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                        DashIconify(
                                                            icon='mdi:exchange',
                                                            width=25
                                                        ),
                                                        html.Br(),
                                                        'Trade Volume'
                                                    ]
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        ),

                        html.Div(
                            children=(
                                html.A(
                                    href='#acknowledged-time-stock',
                                    children=(
                                        html.Div(
                                            className='sidemenu-link-container',
                                            children=(
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                        DashIconify(
                                                            icon='ant-design:stock-outlined',
                                                            width=25
                                                        ),
                                                        html.Br(),
                                                        'Ack\'ed Trade Delay'
                                                    ]
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        ),

                        html.Div(
                            children=(
                                html.A(
                                    href='#heatmap',
                                    children=(
                                        html.Div(
                                            className='sidemenu-link-container',
                                            children=(
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                        DashIconify(
                                                            icon='mdi:hot',
                                                            width=25
                                                        ),
                                                        html.Br(),
                                                        'Fill Rate'
                                                    ]
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        
                        html.Div(
                            children=(
                                html.A(
                                    href='#cancel-time',
                                    children=(
                                        html.Div(
                                            className='sidemenu-link-container',
                                            children=(
                                                html.P(
                                                    className='sidemenu-link',
                                                    children=[
                                                        DashIconify(
                                                            icon='material-symbols:cancel',
                                                            width=25
                                                        ),
                                                        html.Br(),
                                                        'Cancelled Trade Delay'
                                                    ]
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )                        
                    ]
                )                
            )
        ),
        
        html.Div(
            className='main',
            children=(
                html.Div(
                    className='main-container',
                    children=[
                        html.Div(
                            id='treemap',
                            children=[
                                html.H1(
                                    className='text-center',
                                    children='Trade Volume', 
                                ),

                                html.Div(
                                    children=(
                                        dcc.Graph(
                                            id='symbol-treemap',
                                            style={
                                                'height': '43vh',
                                            }
                                        )
                                    )
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
                        ),

                        html.Div(
                            id='acknowledged-time-stock',
                            className='text-center',
                            style={'height':'98vh'},
                            children=[
                                html.H1(
                                    className='text-center',
                                    children='Acknowledged Trade Delay', 
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(
                                            id='bubble-stock-id-acked',
                                            style={
                                                'height':'88vh'
                                            }
                                        )                                    
                                    ]
                                )
                            ]
                        ),
                        
                        html.Div(
                            id='heatmap',
                            children=(
                                html.Div(
                                    className='text-center',
                                    style={
                                        'height':'98vh'
                                    },
                                    children=[
                                        html.H1(
                                            className='text-center',
                                            children='Fill Rate', 
                                        ),

                                        dcc.Graph(
                                            id='fill-rate-heatmap', 
                                            style={'height':'75vh'}, 
                                            figure=get_heatmap_figure(get_df(), DEFAULT_THRESHOLD)
                                        ),

                                        dcc.Input(
                                            id='input-fill-threshold', 
                                            type='number', 
                                            placeholder='60'
                                        ),

                                        html.Button(
                                            id='submit-fill-threshold',
                                            n_clicks=0, 
                                            children='Update'
                                        ),

                                        html.P(
                                            id='current-threshold', 
                                            children=f'Current Threshold: {DEFAULT_THRESHOLD} microseconds'
                                        )
                                    ]
                                )
                            )
                        ),
                        
                        html.Div(
                            id='cancel-time',
                            className='text-center',
                            style={
                                'height':'98vh'
                            },
                            children=[
                                html.H1(
                                    className='text-center',
                                    children='Cancelled Trade Delay'
                                ),
                                dcc.Graph(
                                    id='bubble-stock-id',
                                    style={
                                        'height':'88vh'
                                    }
                                )
                            ]
                        )
                    ]
                )
            )
        ),

        html.Div(
            className='static-data',
            children=(
                html.Div(
                    className='static-data-container',
                    children=(
                        html.Div(
                            children=[
                                html.P(
                                    id='exchange',
                                    children='Choose the exchange you want to analyze'
                                ),
                                dcc.Dropdown(
                                    ['Exchange 1', 'Exchange 2', 'Exchange 3'], 
                                    'Exchange 1', 
                                    id='exchange-dropdown'
                                )
                            ]
                        )
                    )
                )
            )
        )
    ]
)


# Callback for Treemap graph
@app.callback(
    Output('symbol-treemap', 'figure'),
    [Input('exchange', 'children')]
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
    Input('exchange', 'children'),
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
        Input('exchange', 'children'))
def update_output_cancelled(click_data, children):
    if click_data is not None:
        selected_symbol = click_data['points'][0]['label']
        line_fig = get_cancelled_graph(get_df(), current_exchange, selected_symbol)
        return line_fig

    return get_default_line_graph()

# Callbacks for Fill Rate graph
@app.callback(
    Output('fill-rate-heatmap', 'figure'),
    Input('submit-fill-threshold', 'n_clicks'),
    Input('exchange', 'children'),
    State('input-fill-threshold', 'value')
)
def update_heatmap(n_clicks, children, threshold):
    return get_heatmap_figure(get_df(), threshold)

@app.callback(
    Output('current-threshold', 'children'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_current_threshold(n_clicks, threshold):
    return f'Current Threshold: {threshold or DEFAULT_THRESHOLD} microseconds'


# Callback for the exchange dropdownlist
@app.callback(
    Output('exchange', 'children'),
    Input('exchange-dropdown', 'value')
)
def update_output(value):
    set_exchange(value)
    return 'Select the exchange you want to use.'


if __name__ == '__main__':
    app.run(debug=True)
