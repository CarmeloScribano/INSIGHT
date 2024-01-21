from graphs.utils import get_duration_of_x_and_y, get_df_rows_by_symbol
import plotly.graph_objects as go

def get_acked_figure(df, stock_value):
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


    return fig