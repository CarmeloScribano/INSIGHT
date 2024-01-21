import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from .utils import get_trades_by_type, get_df_rows_by_symbol

pd.options.mode.copy_on_write = True

def get_acked_trades(df):
    return get_trades_by_type(df, 'NewOrderAcknowledged')

def get_volume_df(df):
    symbol_counts = get_acked_trades(df)['Symbol'].value_counts()
    treemap_data = pd.DataFrame({'Symbol': symbol_counts.index, 'Count': symbol_counts.values})
    treemap_data['label'] = treemap_data['Symbol']
    return treemap_data

def get_graph_data(df): 
    treemap_data = get_volume_df(df)
    fig = px.treemap(treemap_data, template='plotly_dark', path=['Symbol'], values='Count')
    fig.update_traces(hovertemplate='<b>Stock:</b> %{label}<br><b>Volume Traded:</b> %{value}')
    return fig

def get_line_graph_data(df, selected_symbol, max_points=100):
    stock_data = get_acked_trades(df)
    target_df = get_df_rows_by_symbol(stock_data, selected_symbol)

    target_df['TimeStamp'] = pd.to_datetime(target_df['TimeStamp'])

    target_df.set_index('TimeStamp', inplace=True)

    target_df_copy = target_df.copy()

    resampled_df = target_df_copy.resample('5s').size().reset_index(name='TradeCount')
    resampled_df = resampled_df.tail(max_points)

    fig = go.Figure(data=go.Scatter(x=[resampled_df['TimeStamp'].iloc[0]], y=[resampled_df['TradeCount'].iloc[0]],
                                   mode='markers',
                                   marker=dict(color='rgba(90, 77, 130, 1)', size=10),
                                   name='Trade Count'))
    
    fig.update_layout(template='plotly_dark',
                    title=f'Trade Volume for {selected_symbol}', 
                    xaxis_title='Timestamp',    
                    yaxis_title='Trade Count')

    frames = [
        go.Frame(data=go.Scatter(x=resampled_df['TimeStamp'][:i+1],
                                y=resampled_df['TradeCount'][:i+1],
                                mode='markers',
                                marker=dict(color='rgba(90, 77, 130, 1)', size=10),
                                name='Trade Count'),
                 name=str(i))
        for i in range(1, len(resampled_df)+1)
    ]

    frames.append(go.Frame(data=go.Scatter(x=resampled_df['TimeStamp'],
                                        y=resampled_df['TradeCount'],
                                        mode='lines+markers',
                                        line=dict(color='rgba(90, 77, 130, 1)', width=2),
                                        name='Trade Count'),
                           name='Final'))

    fig.frames = frames

    fig.update_layout(updatemenus=[
        dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Visualize',
                method='animate',
                args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)]
            )],
            x=1,
            y=1.3
        )
    ])

    return fig

def get_default_line_graph():
    fig = go.Figure(data=go.Scatter(x=[''], y=[''],
            mode='markers',
            marker=dict(color='rgba(90, 77, 130, 1)', size=10),
            name='Trade Count'))
    
    fig.update_layout(template='plotly_dark')

    return fig
