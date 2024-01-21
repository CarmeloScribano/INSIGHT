import pandas as pd
from dash import Dash, html, dcc, Output, Input, State
from dash_iconify import DashIconify
from graphs.ingestor import get_data_frame
from graphs.treemap import get_graph_data, get_line_graph_data, get_default_line_graph
from graphs.fill_rate import DEFAULT_THRESHOLD, get_heatmap_figure


pd.options.mode.copy_on_write = True

df = get_data_frame("Exchange_1")

    
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
                                html.Div(
                                    style={'height':'98vh'},
                                    children=[
                                        html.H1(children='Heatmap Test', style={'textAlign':'center'}),
                                        dcc.Graph(id='fill-rate-heatmap', figure=get_heatmap_figure(DEFAULT_THRESHOLD)),
                                        dcc.Input(id='input-fill-threshold', type='number', placeholder='30μs'),
                                        html.Button(id='submit-fill-threshold', n_clicks=0, children='Update'),
                                        html.P(id="test", children=f'Current Threshold: {DEFAULT_THRESHOLD} microseconds')
                                    ]
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


# Callbacks for Fill Rate graph
@app.callback(
    Output('fill-rate-heatmap', 'figure'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_heatmap(n_clicks, threshold):
    return get_heatmap_figure(threshold)

@app.callback(
    Output('test', 'children'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_current_threshold(n_clicks, threshold):
    return f"Current Threshold: {threshold or DEFAULT_THRESHOLD} microseconds"


@app.callback(
    Output('exchange', 'children'),
    Input('exchange-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run(debug=True)
