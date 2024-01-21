from .utils import get_duration_of_x_and_y, get_df_rows_by_symbol
import plotly.graph_objects as go
from datetime import timedelta

def get_cancelled_graph(df, exchange, stock_value):
    dff = get_df_rows_by_symbol(df, stock_value)

    # To be done
    cancel_var = "CancelAcknowledged"
    if exchange == "Exchange 2":
        cancel_var = "Cancelled"

    dff = get_duration_of_x_and_y(dff, "CancelRequest", cancel_var)

    fig = go.Figure(data=go.Scatter(
        x=[dff['TimeStamp_x'].iloc[0]],
        y=[dff['XYDuration'].iloc[0]],
        mode='markers',
        marker=dict(color='rgb(255,255,255)', size=10),
    ))
    fig.update_layout(template="plotly_dark",
                    title=f'Order Cancel Delay for {stock_value}', 
                    xaxis_title='Timestamp',    
                    yaxis_title='Delay (in microseconds)')

    frames = [
        go.Frame(data=go.Scatter(
            x=dff['TimeStamp_x'][:i + 1],
            y=dff['XYDuration'][:i + 1],
            mode='markers',
            marker=dict(color=dff['XYDuration'][:i + 1], colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']], size=10)),
            layout=dict(
                xaxis=dict(range=[min(dff['TimeStamp_x'] - timedelta(seconds=20)), max(dff['TimeStamp_x']) + timedelta(seconds=20)]),
                yaxis=dict(range=[min(dff['XYDuration'] - 100000), max(dff['XYDuration'] + 100000)])
            ),
            name=str(i))
        for i in range(1, len(dff) + 1)
    ]

    fig.frames = frames

    fig.update_layout(
        updatemenus=[dict(type='buttons', showactive=False,
                          buttons=[dict(label='Play',
                                        method='animate',
                                        args=[None, dict(frame=dict(duration=10, redraw=False), fromcurrent=True)])])])
    
    fig.update_layout(xaxis=dict(range=[min(dff['TimeStamp_x'] - timedelta(seconds=20)), max(dff['TimeStamp_x']) + timedelta(seconds=20)]),
                yaxis=dict(range=[min(dff['XYDuration'] - 100000), max(dff['XYDuration'] + 100000)]))

    return fig

# if __name__ == '__main__':
#     app.run(debug=True, port=8050)
