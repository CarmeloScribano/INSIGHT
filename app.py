import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Output, Input, State
from dash_iconify import DashIconify
from graphs.ingestor import get_data_frame
from graphs.utils import get_df_rows_by_symbol, get_duration_of_x_and_y
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
                            id="treemap",
                            children=[
                                html.H1(
                                    className="text-center",
                                    children='Tree Map', 
                                ),

                                html.Div(
                                    children=(
                                        dcc.Graph(
                                            id='symbol-treemap',
                                            style={
                                                "height": "43vh",
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
                                                "height": "43vh",
                                            }
                                        )
                                    )
                                )
                            ]
                        ),
                        
                        html.Div(
                            id='cancel-time',
                            children=[
                                html.H1(
                                    className="text-center",
                                    children='Cancel Time', 
                                ),
                                dcc.Graph(
                                    style={
                                        "height": "88vh",
                                    },
                                    figure=get_graph_data()
                                )
                            ]
                        ),
                        
                        html.Div(
                            id='acknowledged-time-stock',
                            style={'height':'98vh'},
                            children=[
                                html.H1(
                                    className="text-center",
                                    children='Ackowledged Time Stock', 
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(
                                            id='bubble-stock-id-acked',
                                            style={'height':'75vh'}
                                        ),
                                        dcc.Input(
                                            id='input-stock-state-acked', 
                                            type='text', 
                                            value=''
                                        ),
                                        html.Button(
                                            id='submit-stock-state-acked', 
                                            n_clicks=0, 
                                            children='Submit'
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        html.Div(
                            id='acknowledged-time-exchange',
                            children=[
                                html.H1(
                                    className="text-center",
                                    children='Ackowledged Time Exchange', 
                                ),
                                dcc.Graph(
                                    style={
                                        "height": "88vh",
                                    },
                                    figure=get_graph_data()
                                )
                            ]
                        ),
                        
                        html.Div(
                            id='heatmap',
                            children=(
                                html.Div(
                                    className="text-center",
                                    style={'height':'98vh'},
                                    children=[
                                        html.H1(
                                            className="text-center",
                                            children='Heatmap Test', 
                                        ),
                                        dcc.Graph(
                                            id='fill-rate-heatmap', 
                                            style={'height':'75vh'}, 
                                            figure=get_heatmap_figure(DEFAULT_THRESHOLD)
                                        ),
                                        dcc.Input(
                                            id='input-fill-threshold', 
                                            type='number', 
                                            placeholder='30μs'
                                        ),
                                        html.Button(
                                            id='submit-fill-threshold',
                                            n_clicks=0, 
                                            children='Update'
                                        ),
                                        html.P(
                                            id="current-threshold", 
                                            children=f'Current Threshold: {DEFAULT_THRESHOLD} microseconds'
                                        )
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


# Callback for Treemap graph
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


# Callbacks for Acked graph
@app.callback(
        Output('bubble-stock-id-acked', 'figure'),
        Input('submit-stock-state-acked', 'n_clicks'),
        State('input-stock-state-acked', 'value'))
def update_output(n_clicks, stock_value):
    dff = get_df_rows_by_symbol(df, stock_value)

    dff = get_duration_of_x_and_y(dff, "NewOrderRequest", "NewOrderAcknowledged")

    fig = go.Figure(data=go.Scatter(
        x=dff['TimeStamp_x'],
        y=dff['XYDuration'],
        mode='markers',
        marker=dict(color=dff['XYDuration'], colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']], size=10),
    ))
    fig.update_layout(template="plotly_dark")

    frames = [
        go.Frame(data=go.Scatter(
            x=dff['TimeStamp_x'][:i + 1],
            y=dff['XYDuration'][:i + 1],
            mode='markers',
            marker=dict(color=dff['XYDuration'][:i + 1], colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']], size=10),
            name='Trade Count'),
            name=str(i))
        for i in range(1, len(dff) + 1)
    ]

    fig.frames = frames

    fig.update_layout(
        updatemenus=[dict(type='buttons', showactive=False,
                          buttons=[dict(label='Play',
                                        method='animate',
                                        args=[None, dict(frame=dict(duration=150, redraw=True), fromcurrent=True)])])])



# Callbacks for Fill Rate graph
@app.callback(
    Output('fill-rate-heatmap', 'figure'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_heatmap(n_clicks, threshold):
    return get_heatmap_figure(threshold)

@app.callback(
    Output('current-threshold', 'children'),
    Input('submit-fill-threshold', 'n_clicks'),
    State('input-fill-threshold', 'value')
)
def update_current_threshold(n_clicks, threshold):
    return f"Current Threshold: {threshold or DEFAULT_THRESHOLD} microseconds"


# Callback for the exchange dropdownlist
@app.callback(
    Output('exchange', 'children'),
    Input('exchange-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run(debug=True)
