from ingestor import get_data_frame
from utils import get_duration_of_x_and_y, get_df_rows_by_symbol
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go
import pandas as pd

exchange = "Exchange_2"
df = get_data_frame(exchange)

is_anim_playing = False

app = Dash(__name__)

app.layout = html.Div([
    html.Div("Cancel orders within a Scatter plot"),
    dcc.Input(id='input-stock-state-canceled', type='text', value=''),
    html.Button(id='submit-stock-state', n_clicks=0, children='Submit'),
    dcc.Graph(id='bubble-stock-id')])

@app.callback(
        Output('bubble-stock-id', 'figure'),
        Input('submit-stock-state', 'n_clicks'),
        State('input-stock-state-canceled', 'value'))
def update_output(n_clicks, stock_value):
    dff = get_df_rows_by_symbol(df, stock_value)

    cancel_var = "CancelAcknowledged"
    if exchange == "Exchange_2":
        cancel_var = "Cancelled"

    dff = get_duration_of_x_and_y(dff, "CancelRequest", cancel_var)

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


    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
